from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, transaction
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from .models import Appointment, Customer
from .views_appointment import (
    _staff_options,
    _service_options,
    _normalize_services,
    _services_prices_and_total,
    _load_appointment_service_rows,
    _norm_hms_str,
)

# -------- My Appointments List --------
@login_required
def my_appointment_list(request):
    # Find the logged-in user's customer_id
    customer = get_object_or_404(Customer, user_id=request.user.id)

    with connection.cursor() as c:
        c.execute("""
            SELECT a.appointment_id, a.appointment_date, a.start_time, a.end_time,
                   a.status, a.total_amount,
                   CONCAT(s.first_name,' ',s.last_name) AS staff_name
            FROM APPOINTMENT a, STAFF s  
            WHERE a.staff_id = s.staff_id 
            AND a.customer_id = %s 
            ORDER BY a.appointment_date DESC, a.start_time DESC, a.appointment_id DESC
        """, [customer.customer_id])
        rows = c.fetchall()

    appts = [{
        'id': r[0], 'date': r[1], 'start': r[2], 'end': r[3],
        'status': r[4], 'total': r[5], 'staff': r[6]
    } for r in rows]

    return render(request, 'appointments/my_appointments.html', {'appointments': appts})


# -------- Add My Appointment --------
@login_required
@transaction.atomic
def my_appointment_add(request):
    staff_opts = _staff_options()
    svc_opts = _service_options()

    customer = get_object_or_404(Customer, user_id=request.user.id)

    if request.method == 'POST':
        appointment_date = (request.POST.get("appointment_date") or "").strip()
        start_time = (request.POST.get("start_time") or "").strip()

        if not appointment_date or not start_time:
            messages.error(request, "Please pick a date and a time.")
            return render(request, 'appointments/my_appointment_add.html', {
            'staff_opts': staff_opts,
            'svc_opts': svc_opts
        })

        start_dt = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        end_time = (start_dt + timedelta(minutes=90)).strftime("%H:%M:%S")
        # date_time_result, error_response = _parse_start_end_time(
        #     request,
        #     'appointments/my_appointment_add.html',
        #     {'staff_opts': staff_opts, 'svc_opts': svc_opts}
        # )
        # if error_response:
        #     return error_response
        # appointment_date, start_time, end_time = date_time_result
        staff_id = request.POST.get('staff_id')
        # appointment_date = request.POST.get('appointment_date')
        # start_time = request.POST.get('start_time')
        # end_time = request.POST.get('end_time') or None
        notes = request.POST.get('notes', '').strip() or None

        raw_service_ids = request.POST.getlist('service_ids[]')
        raw_colors = request.POST.getlist('polish_colors[]')

        service_ids, polish_colors = _normalize_services(raw_service_ids, raw_colors)
        price_map, total_amount = _services_prices_and_total(service_ids)

        # Always pending
        appt = Appointment.objects.create(
            customer_id=customer.customer_id,
            staff_id=staff_id,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            status="pending",
            total_amount=total_amount,
            notes=notes,
            created_date=timezone.now(),
        )

        if service_ids:
            with connection.cursor() as c:
                for idx, sid in enumerate(service_ids):
                    c.execute(
                        """
                        INSERT INTO APPOINTMENT_SERVICE
                            (appointment_id, service_id, service_price, polish_color)
                        VALUES (%s, %s, %s, %s)
                        """,
                        [appt.appointment_id, sid, price_map.get(sid, 0), polish_colors[idx]]
                    )

        messages.success(request, 'Appointment created and set to pending.')
        return redirect('my_appointments')

    return render(request, 'appointments/my_appointment_add.html', {
        'staff_opts': staff_opts,
        'svc_opts': svc_opts,
    })


# -------- Edit My Appointment --------
@login_required
@transaction.atomic
def my_appointment_edit(request, appointment_id):
    customer = get_object_or_404(Customer, user_id=request.user.id)
    appt = get_object_or_404(Appointment, pk=appointment_id, customer_id=customer.customer_id)

    if appt.status not in ["pending", "scheduled"]:
        messages.error(request, 'You can only edit pending or scheduled appointments.')
        return redirect('my_appointments')

    staff_opts = _staff_options()
    svc_opts = _service_options()

    time_slots = [
        ("09:00:00", "9:00 AM"),
        ("10:30:00", "10:30 AM"),
        ("12:00:00", "12:00 PM"),
        ("13:30:00", "1:30 PM"),
        ("15:00:00", "3:00 PM"),
        ("18:30:00", "6:30 PM"),
    ]

    # Normalize and snap the existing start_time to one of the slots (if possible)
    normalized = _norm_hms_str(appt.start_time)
    slot_values = [t for (t, _) in time_slots]
    selected_time = normalized if normalized in slot_values else ""

    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        appointment_date = (request.POST.get('appointment_date') or '').strip()
        start_time = _norm_hms_str((request.POST.get('start_time') or '').strip())
        notes = request.POST.get('notes', '').strip() or None

        if not appointment_date or not start_time:
            messages.error(request, "Please pick a date and a time.")
            current_services = _load_appointment_service_rows(appt.appointment_id)
            return render(request, 'appointments/my_appointment_edit.html', {
                'appt': appt,
                'staff_opts': staff_opts,
                'svc_opts': svc_opts,
                'current_services': current_services,
                'time_slots': time_slots,
                'selected_time': selected_time,  # keep highlight
            })

        start_dt = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        end_time = (start_dt + timedelta(minutes=90)).strftime("%H:%M:%S")

        raw_service_ids = request.POST.getlist('service_ids[]')
        raw_colors = request.POST.getlist('polish_colors[]')
        service_ids, colors = _normalize_services(raw_service_ids, raw_colors)
        price_map, total_amount = _services_prices_and_total(service_ids)

        appt.staff_id = staff_id
        appt.appointment_date = appointment_date
        appt.start_time = start_time
        appt.end_time = end_time
        appt.notes = notes
        appt.total_amount = total_amount
        appt.status = "pending"
        appt.save()

        with connection.cursor() as c:
            c.execute("DELETE FROM APPOINTMENT_SERVICE WHERE appointment_id = %s", [appt.appointment_id])
            for idx, sid in enumerate(service_ids):
                c.execute(
                    """
                    INSERT INTO APPOINTMENT_SERVICE
                        (appointment_id, service_id, service_price, polish_color)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [appt.appointment_id, sid, price_map.get(sid, 0), colors[idx]]
                )

        messages.success(request, 'Appointment updated and set to pending.')
        return redirect('my_appointments')

    # GET
    current_services = _load_appointment_service_rows(appt.appointment_id)
    return render(request, 'appointments/my_appointment_edit.html', {
        'appt': appt,
        'staff_opts': staff_opts,
        'svc_opts': svc_opts,
        'current_services': current_services,
        'time_slots': time_slots,
        'selected_time': selected_time,  # exact HH:MM:SS or ''
    })
