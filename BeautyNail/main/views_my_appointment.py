from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, transaction
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

from .models import Appointment, Customer, Review
from .views_appointment import (
    _staff_options,
    _service_options,
    _normalize_services,
    _services_price_amount_and_minutes,  # <-- NEW helper name
    _load_appointment_service_rows,
    _norm_hms_str,
)

# -------- My Appointments List --------

def get_my_appointments_by_search(customer_id, query):
    sql = """
        SELECT
            a.appointment_id,                 -- PK for .raw()
            a.appointment_id AS id,
            a.appointment_date AS date,
            a.start_time       AS start,
            a.end_time         AS end,
            a.status,
            a.total_amount     AS total,
            CONCAT(s.first_name, ' ', s.last_name) AS staff_name,
            r.review_id AS review_id          -- NULL if no review
        FROM appointment a
        JOIN staff s
          ON a.staff_id = s.staff_id
        LEFT JOIN review r
          ON r.appointment_id = a.appointment_id
         AND r.customer_id    = %s
        WHERE a.customer_id = %s
    """
    params = [customer_id, customer_id]

    if query:
        sql += """
          AND (
                s.first_name LIKE %s OR s.last_name LIKE %s OR
                a.status LIKE %s OR
                DATE_FORMAT(a.appointment_date,'%%Y-%%m-%%d') = %s OR
                CAST(a.appointment_id AS CHAR) = %s
          )
        """
        like = f"%{query}%"
        params += [like, like, like, query, query]

    sql += " ORDER BY a.appointment_date DESC, a.start_time DESC, a.appointment_id DESC "
    return Appointment.objects.raw(sql, params)

@login_required
def my_appointment_list(request):
    user_id = request.user.id if hasattr(request.user, "id") else request.user
    customer = get_object_or_404(Customer, user_id=user_id)

    query = (request.GET.get("search") or "").strip()
    appointments = get_my_appointments_by_search(customer.customer_id, query)

    return render(request, "appointments/my_appointments.html", {
        "appointments": appointments,
        "search_query": query,
    })

# -------- Add My Appointment --------
@login_required
@transaction.atomic
def my_appointment_add(request):
    staff_opts = _staff_options()
    svc_opts = _service_options()

    customer = get_object_or_404(Customer, user_id=request.user.id)

    if request.method == 'POST':
        appointment_date = (request.POST.get("appointment_date") or "").strip()
        start_time_raw   = (request.POST.get("start_time") or "").strip()
        start_time       = _norm_hms_str(start_time_raw)  # normalize "9:00" => "09:00:00"

        if not appointment_date or not start_time:
            messages.error(request, "Please pick a date and a time.")
            return render(request, 'appointments/my_appointment_add.html', {
                'staff_opts': staff_opts,
                'svc_opts': svc_opts
            })

        staff_id = request.POST.get('staff_id')
        notes    = (request.POST.get('notes') or '').strip() or None

        raw_service_ids = request.POST.getlist('service_ids[]')
        raw_colors      = request.POST.getlist('polish_colors[]')
        service_ids, polish_colors = _normalize_services(raw_service_ids, raw_colors)

        # NEW: prices + total + summed duration
        price_map, total_amount, total_minutes = _services_price_amount_and_minutes(service_ids)

        # Compute end_time from durations (fallback 90 if none)
        start_dt = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        minutes  = total_minutes
        end_time = (start_dt + timedelta(minutes=minutes)).strftime("%H:%M:%S")

        # Always create as pending
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
    svc_opts   = _service_options()

    time_slots = [
        ("09:00:00", "9:00 AM"),
        ("10:30:00", "10:30 AM"),
        ("12:00:00", "12:00 PM"),
        ("13:30:00", "1:30 PM"),
        ("15:00:00", "3:00 PM"),
        ("18:30:00", "6:30 PM"),
    ]

    # Normalize and snap the existing start_time to one of the slots (if possible)
    normalized    = _norm_hms_str(appt.start_time)
    slot_values   = [t for (t, _) in time_slots]
    selected_time = normalized if normalized in slot_values else ""

    if request.method == 'POST':
        staff_id        = request.POST.get('staff_id')
        appointment_date = (request.POST.get('appointment_date') or '').strip()
        start_time       = _norm_hms_str((request.POST.get('start_time') or '').strip())
        notes            = (request.POST.get('notes') or '').strip() or None

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

        raw_service_ids = request.POST.getlist('service_ids[]')
        raw_colors      = request.POST.getlist('polish_colors[]')
        service_ids, colors = _normalize_services(raw_service_ids, raw_colors)

        # NEW: prices + total + summed duration
        price_map, total_amount, total_minutes = _services_price_amount_and_minutes(service_ids)

        # Compute end_time from durations (fallback 90 if none)
        start_dt = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        minutes  = total_minutes
        end_time = (start_dt + timedelta(minutes=minutes)).strftime("%H:%M:%S")

        # Apply updates
        appt.staff_id         = staff_id
        appt.appointment_date = appointment_date
        appt.start_time       = start_time
        appt.end_time         = end_time
        appt.notes            = notes
        appt.total_amount     = total_amount
        appt.status           = "pending"
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

# -------- Reviews --------

@login_required
def my_review_add(request, appointment_id):
    # Ensure this appointment belongs to the logged-in customer and is completed
    customer = get_object_or_404(Customer, user_id=request.user.id)
    appt = get_object_or_404(Appointment, pk=appointment_id, customer_id=customer.customer_id)

    if (appt.status or '').lower() != 'completed':
        messages.error(request, 'You can only review completed appointments.')
        return redirect('my_appointments')

    # If a review already exists, go to edit
    existing = Review.objects.filter(customer_id=customer.customer_id, appointment_id=appt.appointment_id).first()
    if existing:
        return redirect('my_review_edit', review_id=existing.review_id)

    # Display staff name (optional)
    with connection.cursor() as c:
        c.execute("SELECT CONCAT(first_name,' ',last_name) FROM STAFF WHERE staff_id = %s", [appt.staff_id])
        row = c.fetchone()
    staff_name = row[0] if row else "-"

    if request.method == 'POST':
        rating  = request.POST.get('rating')
        comment = (request.POST.get('comment') or '').strip() or None

        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError()
        except Exception:
            messages.error(request, 'Please choose a rating between 1 and 5.')
            return render(request, 'reviews/my_review_add.html', {
                'appt': appt,
                'staff_name': staff_name,
            })

        Review.objects.create(
            customer_id=customer.customer_id,
            appointment_id=appt.appointment_id,
            staff_id=appt.staff_id,
            rating=rating_int,
            comment=comment,
            review_date=timezone.now(),
        )
        messages.success(request, 'Review submitted. Thank you!')
        return redirect('my_appointments')

    return render(request, 'reviews/my_review_add.html', {
        'appt': appt,
        'staff_name': staff_name,
    })

@login_required
def my_review_edit(request, review_id):
    customer = get_object_or_404(Customer, user_id=request.user.id)
    item = get_object_or_404(Review, pk=review_id, customer_id=customer.customer_id)

    # Optional: verify the appointment is still completed
    appt = get_object_or_404(Appointment, pk=item.appointment_id, customer_id=customer.customer_id)

    if request.method == 'POST':
        rating  = request.POST.get('rating')
        comment = (request.POST.get('comment') or '').strip() or None

        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError()
        except Exception:
            messages.error(request, 'Please choose a rating between 1 and 5.')
            return render(request, 'reviews/my_review_edit.html', {'item': item, 'appt': appt})

        item.rating = rating_int
        item.comment = comment
        item.review_date = timezone.now()
        item.save()

        messages.success(request, 'Review updated.')
        return redirect('my_appointments')

    return render(request, 'reviews/my_review_edit.html', {'item': item, 'appt': appt})
