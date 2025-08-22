# views_guest.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, transaction
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from .models import Appointment, Customer
from .views_appointment import (
    _staff_options,
    _service_options,
    _normalize_services,
    _services_price_amount_and_minutes,  
    _norm_hms_str,                        # <-- normalize "9:00" => "09:00:00"
)

@transaction.atomic
def guest_appointment_add(request):
    """
    Public booking page with simple confirm popup.
    On confirm (confirm_booking=1):
      1) create/get auth User (username=email; password=phone if created)
      2) create/get Customer linked to that user
      3) create Appointment (+ APPOINTMENT_SERVICE rows)
    Then redirect to a success/summary page.
    """
    staff_opts = _staff_options()
    svc_opts   = _service_options()

    if request.method == 'POST':
        # Identity + basics
        first_name = (request.POST.get('first_name') or '').strip()
        last_name  = (request.POST.get('last_name') or '').strip()
        email      = (request.POST.get('email') or '').strip()
        phone      = (request.POST.get('phone') or '').strip()
        staff_id   = (request.POST.get('staff_id') or '').strip()
        notes      = (request.POST.get('notes') or '').strip() or None

        # Date/time (from form/JS)
        appointment_date = (request.POST.get('appointment_date') or '').strip()
        start_time_raw   = (request.POST.get('start_time') or '').strip()
        start_time       = _norm_hms_str(start_time_raw)

        # Validate required fields
        if not (first_name and last_name and email and phone and staff_id):
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'appointments/guest_appointment_add.html', {
                'staff_opts': staff_opts, 'svc_opts': svc_opts,
            })
        if not (appointment_date and start_time):
            messages.error(request, 'Please pick a valid date and time.')
            return render(request, 'appointments/guest_appointment_add.html', {
                'staff_opts': staff_opts, 'svc_opts': svc_opts,
            })
        if (request.POST.get('confirm_booking') or '') != '1':
            messages.info(request, 'Please confirm your booking.')
            return render(request, 'appointments/guest_appointment_add.html', {
                'staff_opts': staff_opts, 'svc_opts': svc_opts,
            })

        # Services (multi-select with "unsure")
        raw_service_ids = request.POST.getlist('service_ids[]')
        raw_colors      = request.POST.getlist('polish_colors[]')
        unsure_selected = any((sid or '').strip() == 'unsure' for sid in raw_service_ids)
        if unsure_selected:
            service_ids, colors = [], []
        else:
            service_ids, colors = _normalize_services(raw_service_ids, raw_colors)

        # Compute price + total + summed duration (minutes)
        price_map, total_amount, total_minutes = _services_price_amount_and_minutes(service_ids)

        # 1) Auth user (username=email)
        user, created_user = User.objects.get_or_create(
            username=email,
            defaults={'email': email, 'first_name': first_name, 'last_name': last_name}
        )
        if created_user:
            user.set_password(phone)   # password = phone number (as in your original flow)
            user.save()

        # 2) Customer (link to auth user)
        customer, created_customer = Customer.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'user_id': user.id,
                'is_active': True,
                'loyalty_points': 0,
            }
        )
        if not created_customer:
            if not customer.user_id:
                customer.user_id = user.id
            if not customer.phone and phone:
                customer.phone = phone
            if not customer.first_name and first_name:
                customer.first_name = first_name
            if not customer.last_name and last_name:
                customer.last_name = last_name
            customer.save()

        # 3) Appointment — end_time from summed duration (fallback 90 mins)
        start_dt = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        minutes  = total_minutes
        end_time = (start_dt + timedelta(minutes=minutes)).strftime("%H:%M:%S")

        appt = Appointment.objects.create(
            customer_id=customer.customer_id,
            staff_id=staff_id,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            status='pending',
            total_amount=total_amount,
            notes=notes,
            created_date=timezone.now(),
        )

        # Insert APPOINTMENT_SERVICE rows
        if service_ids:
            with connection.cursor() as c:
                for idx, sid in enumerate(service_ids):
                    c.execute(
                        """
                        INSERT INTO APPOINTMENT_SERVICE
                            (appointment_id, service_id, service_price, polish_color)
                        VALUES (%s, %s, %s, %s)
                        """,
                        [appt.appointment_id, sid, price_map.get(sid, 0), colors[idx]]
                    )

        # Go to success page with summary
        return redirect('guest_appointment_success', appointment_id=appt.appointment_id)

    # GET
    return render(request, 'appointments/guest_appointment_add.html', {
        'staff_opts': staff_opts, 'svc_opts': svc_opts,
    })


def guest_appointment_success(request, appointment_id: int):
    """
    Show a summary page for the created appointment.
    """
    # Ensure the appointment exists
    appt = get_object_or_404(Appointment, pk=appointment_id)

    # Load joined info (staff/customer)
    with connection.cursor() as c:
        c.execute(
            """
            SELECT a.appointment_id,
                   a.appointment_date,
                   a.start_time,
                   a.end_time,
                   a.status,
                   a.total_amount,
                   c.first_name, c.last_name, c.email, c.phone,
                   CONCAT(s.first_name,' ',s.last_name) AS staff_name
            FROM appointment a, customer c, staff s
            WHERE  a.customer_id = c.customer_id
            AND    a.staff_id    = s.staff_id
            AND    a.appointment_id = %s
            """,
            [appointment_id]
        )
        row = c.fetchone()

        c.execute(
            """
            SELECT sv.service_name, aps.service_price, aps.polish_color
            FROM appointment_service aps, service sv
            WHERE aps.service_id = sv.service_id
            AND aps.appointment_id = %s
            ORDER BY sv.service_name ASC
            """,
            [appointment_id]
        )
        svc_rows = c.fetchall()

    item = {
        "id": row[0],
        "date": row[1],
        "start": row[2],
        "end": row[3],
        "status": row[4],
        "total": row[5],
        "cust_first": row[6],
        "cust_last": row[7],
        "cust_email": row[8],
        "cust_phone": row[9],
        "staff_name": row[10],
        "services": [
            {"name": r[0], "price": r[1], "color": r[2]} for r in svc_rows
        ]
    }

    return render(request, "appointments/guest_appointment_success.html", {"item": item})
