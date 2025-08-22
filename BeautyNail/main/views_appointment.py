from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, transaction
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
from datetime import datetime, timedelta, time, date
import re
from decimal import Decimal

from .models import Appointment, Payment, Customer

# ---------- constants ----------
STATUS_CHOICES = ["scheduled", "completed", "cancelled", "pending"]

# ---------- option loaders ----------

def _staff_options():
    with connection.cursor() as c:
        c.execute("""
            SELECT staff_id, first_name, last_name, COALESCE(specialty,'') AS specialty
            FROM STAFF
            WHERE is_active = 1
            ORDER BY last_name, first_name
        """)
        rows = c.fetchall()
    return [{'id': r[0], 'name': f"{r[1]} {r[2]}", 'specialty': r[3]} for r in rows]

def _customer_options():
    with connection.cursor() as c:
        c.execute("""
            SELECT customer_id, first_name, last_name
            FROM CUSTOMER
            ORDER BY last_name, first_name
        """)
        rows = c.fetchall()
    return [{'id': r[0], 'name': f"{r[1]} {r[2]}"} for r in rows]

def _service_options():
    with connection.cursor() as c:
        c.execute("""
            SELECT service_id, service_name, base_price, COALESCE(duration_minutes, 0) AS dur
            FROM SERVICE
            ORDER BY category, service_name
        """)
        rows = c.fetchall()
    return [{'id': r[0], 'name': r[1], 'price': r[2], 'dur': int(r[3] or 0)} for r in rows]

# ---------- helpers (DRY) ----------

def _calc_total_from_services(appointment_id):
    """Fallback: sum APPOINTMENT_SERVICE.service_price if APPOINTMENT.total_amount is NULL."""
    with connection.cursor() as c:
        c.execute("""
            SELECT COALESCE(SUM(service_price), 0)
            FROM APPOINTMENT_SERVICE
            WHERE appointment_id = %s
        """, [appointment_id])
        row = c.fetchone()
    return Decimal(row[0] or 0)

def _service_price_map(service_ids):
    """Return {service_id: base_price} for given ids (ints)."""
    if not service_ids:
        return {}
    placeholders = ",".join(["%s"] * len(service_ids))
    sql = f"SELECT service_id, base_price FROM SERVICE WHERE service_id IN ({placeholders})"
    with connection.cursor() as c:
        c.execute(sql, service_ids)
        rows = c.fetchall()
    return {row[0]: row[1] for row in rows}

def _service_duration_map(service_ids):
    """Return {service_id: duration_minutes(int)} for given ids."""
    if not service_ids:
        return {}
    placeholders = ",".join(["%s"] * len(service_ids))
    sql = f"""
        SELECT service_id, COALESCE(duration_minutes, 0)
        FROM SERVICE
        WHERE service_id IN ({placeholders})
    """
    with connection.cursor() as c:
        c.execute(sql, service_ids)
        rows = c.fetchall()
    return {row[0]: int(row[1] or 0) for row in rows}

def _services_price_amount_and_minutes(service_ids):
    """
    Given service_ids, return:
      - price_map: {service_id -> Decimal}
      - total_amount: Decimal | None (sum of base_price)
      - total_minutes: int (sum of duration_minutes)
    """
    if not service_ids:
        return {}, None, 0
    price_map    = _service_price_map(service_ids)
    duration_map = _service_duration_map(service_ids)
    total_amount = sum(price_map.get(sid, 0) for sid in service_ids) or None
    total_minutes = sum(int(duration_map.get(sid, 0)) for sid in service_ids)
    return price_map, total_amount, total_minutes

def _normalize_services(raw_service_ids, raw_colors):
    """
    Aligns service_ids[] and polish_colors[] by index.
    Filters out empty/invalid service ids.
    Returns (service_ids:list[int], colors:list[str|None])
    """
    service_ids, colors = [], []
    for i, sid in enumerate(raw_service_ids or []):
        sid = (sid or '').strip()
        if not sid.isdigit():
            continue
        service_ids.append(int(sid))
        col = (raw_colors[i] if i < len(raw_colors) else '')
        colors.append((col or '').strip() or None)
    return service_ids, colors

def _load_appointment_service_rows(appointment_id):
    """
    Returns a list of dicts for existing rows to preload in edit:
    [{'service_id': 3, 'service_name': 'Pedicure', 'price': Decimal('30.00'), 'color': 'Red'}, ...]
    """
    with connection.cursor() as c:
        c.execute("""
            SELECT aps.service_id, s.service_name, aps.service_price, aps.polish_color
            FROM APPOINTMENT_SERVICE aps, SERVICE s
            WHERE aps.service_id = s.service_id
              AND aps.appointment_id = %s
            ORDER BY aps.appointment_service_id;
        """, [appointment_id])
        rows = c.fetchall()
    return [{'service_id': r[0], 'service_name': r[1], 'price': r[2], 'color': r[3]} for r in rows]

def _norm_hms_str(val: str) -> str:
    """
    Normalize any 'H:MM' / 'HH:MM' / 'H:MM:SS' / 'HH:MM:SS' to zero-padded 'HH:MM:SS'.
    Returns '' if cannot parse.
    """
    if val is None:
        return ""
    s = str(val).strip()

    # If it's a datetime.time, just format it
    if isinstance(val, time):
        return val.strftime("%H:%M:%S")

    # Pad leading hour if like '9:00' or '9:00:00'
    if re.match(r"^\d:\d{2}(:\d{2})?$", s):
        s = "0" + s  # -> '09:00' or '09:00:00'

    # Try strict parses
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%H:%M:%S")
        except ValueError:
            continue

    # Last resort: if looks like 'HH:MM:SSxxxx', trim to first 8
    if re.match(r"^\d{2}:\d{2}:\d{2}", s):
        return s[:8]

    return ""

ADMIN_TIME_SLOTS = [
    ("09:00:00", "9:00 AM"),
    ("10:30:00", "10:30 AM"),
    ("12:00:00", "12:00 PM"),
    ("13:30:00", "1:30 PM"),
    ("15:00:00", "3:00 PM"),
    ("18:30:00", "6:30 PM"),
]

# ---------- list ----------

def get_appointments_by_status(status_str):
    """
    Case-insensitive filter by status: pending/completed/scheduled/cancelled.
    """
    sql = """
        SELECT
            a.appointment_id,
            a.appointment_id AS id,
            a.appointment_date AS date,
            a.start_time       AS start,
            a.end_time         AS end,
            a.status,
            a.total_amount     AS total,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            CONCAT(s.first_name, ' ', s.last_name) AS staff_name
        FROM appointment a, customer c, staff s
        WHERE a.customer_id = c.customer_id
          AND a.staff_id    = s.staff_id
          AND LOWER(a.status) = LOWER(%s)
        ORDER BY a.appointment_date DESC, a.start_time DESC, a.appointment_id DESC
    """
    return Appointment.objects.raw(sql, [status_str.strip()])

def get_appointments_by_date(day_str):
    """
    Return appointments for a single calendar date (YYYY-MM-DD).
    """
    sql = """
        SELECT
            a.appointment_id,
            a.appointment_id AS id,
            a.appointment_date AS date,
            a.start_time       AS start,
            a.end_time         AS end,
            a.status,
            a.total_amount     AS total,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            CONCAT(s.first_name, ' ', s.last_name) AS staff_name
        FROM appointment a, customer c, staff s
        WHERE a.customer_id = c.customer_id
          AND a.staff_id    = s.staff_id
          AND a.appointment_date = %s
        ORDER BY a.appointment_date DESC, a.start_time DESC, a.appointment_id DESC
    """
    return Appointment.objects.raw(sql, [day_str])

def get_appointments_by_search(query):
    sql = """
        SELECT
            a.appointment_id,
            a.appointment_id AS id,
            a.appointment_date AS date,
            a.start_time       AS start,
            a.end_time         AS end,
            a.status,
            a.total_amount     AS total,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            CONCAT(s.first_name, ' ', s.last_name) AS staff_name
        FROM appointment a, customer c, staff s
        WHERE a.customer_id = c.customer_id
          AND a.staff_id    = s.staff_id
    """
    params = []
    if query:
        sql += """
          AND (
                c.first_name LIKE %s OR c.last_name LIKE %s OR
                s.first_name LIKE %s OR s.last_name LIKE %s OR
                a.status LIKE %s OR
                DATE_FORMAT(a.appointment_date,'%%Y-%%m-%%d') = %s OR
                CAST(a.appointment_id AS CHAR) = %s
          )
        """
        like = f"%{query}%"
        params = [like, like, like, like, like, query, query]

    sql += " ORDER BY a.appointment_date DESC, a.start_time DESC, a.appointment_id DESC "
    return Appointment.objects.raw(sql, params)

def appointment_list(request):
    query = (request.GET.get('search') or '').strip()

    # date filter
    filter_by_date = request.GET.get('filter_by_date')
    selected_date = request.GET.get('appt_date')
    if not selected_date:
        selected_date = date.today().isoformat()

    # status filter
    show_by_status = request.GET.get('show_by_status')
    selected_status = (request.GET.get('status') or '').strip()

    if show_by_status and selected_status:
        appointments = get_appointments_by_status(selected_status)
    elif filter_by_date:
        appointments = get_appointments_by_date(selected_date)
    else:
        appointments = get_appointments_by_search(query)

    return render(request, 'appointments/appointments.html', {
        'appointments': appointments,
        'search_query': query,
        'selected_date': selected_date,
        'status_choices': STATUS_CHOICES,
        'selected_status': selected_status,
    })

# ---------- create ----------

@transaction.atomic
def appointment_add(request):
    staff_opts = _staff_options()
    cust_opts = _customer_options()
    svc_opts = _service_options()

    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        staff_id = request.POST.get('staff_id')
        appointment_date = (request.POST.get('appointment_date') or '').strip()
        start_time = _norm_hms_str((request.POST.get('start_time') or '').strip())
        # allow explicit override, else auto-calc from durations
        end_time = (request.POST.get('end_time') or '').strip() or None
        status = (request.POST.get('status') or 'scheduled').strip() or 'scheduled'
        notes = request.POST.get('notes', '').strip() or None

        raw_service_ids = request.POST.getlist('service_ids[]')
        raw_colors = request.POST.getlist('polish_colors[]')
        service_ids, polish_colors = _normalize_services(raw_service_ids, raw_colors)

        # prices + total + duration minutes
        price_map, total_amount, total_minutes = _services_price_amount_and_minutes(service_ids)

        
        if not appointment_date or not start_time:
            messages.error(request, "Please pick a date and a time.")
            return render(request, 'appointments/appointment_add.html', {
                'staff_opts': staff_opts,
                'cust_opts': cust_opts,
                'svc_opts': svc_opts,
                'status_choices': STATUS_CHOICES,
            })

        # compute end_time if missing: start + sum(duration_minutes)
        if not end_time:
            start_dt = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S")
            minutes = total_minutes
            end_time = (start_dt + timedelta(minutes=minutes)).strftime("%H:%M:%S")

        appt = Appointment.objects.create(
            customer_id=customer_id,
            staff_id=staff_id,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            status=status,
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

        messages.success(request, 'Appointment created.')
        return redirect('appointment_list')

    # GET
    return render(request, 'appointments/appointment_add.html', {
        'staff_opts': staff_opts,
        'cust_opts': cust_opts,
        'svc_opts': svc_opts,
        'status_choices': STATUS_CHOICES,
    })

# ---------- edit ----------

@transaction.atomic
def appointment_edit(request, appointment_id):
    appt = get_object_or_404(Appointment, pk=appointment_id)

    staff_opts = _staff_options()
    cust_opts  = _customer_options()
    svc_opts   = _service_options()

    
    time_slots = [
        ("09:00:00", "9:00 AM"),
        ("10:30:00", "10:30 AM"),
        ("12:00:00", "12:00 PM"),
        ("13:30:00", "1:30 PM"),
        ("15:00:00", "3:00 PM"),
        ("18:30:00", "6:30 PM"),
    ]

    if request.method == 'POST':
        appt.customer_id      = request.POST.get('customer_id')
        appt.staff_id         = request.POST.get('staff_id')
        appointment_date      = (request.POST.get('appointment_date') or '').strip()
        start_time            = _norm_hms_str((request.POST.get('start_time') or '').strip())
        notes                 = request.POST.get('notes', '').strip() or None
        status                = (request.POST.get('status') or appt.status).strip()

        # Require date + time
        if not appointment_date or not start_time:
            messages.error(request, "Please pick a date and a time.")
            current_services = _load_appointment_service_rows(appt.appointment_id)

            # Keep grid highlight
            slot_values   = [t for (t, _) in time_slots]
            selected_time = start_time if start_time in slot_values else ""

            return render(request, 'appointments/appointment_edit.html', {
                'appt': appt,
                'staff_opts': staff_opts,
                'cust_opts': cust_opts,
                'svc_opts': svc_opts,
                'current_services': current_services,
                'time_slots': time_slots,
                'selected_time': selected_time,
                'status_choices': STATUS_CHOICES,
            })

        # Services + totals
        raw_service_ids = request.POST.getlist('service_ids[]')
        raw_colors      = request.POST.getlist('polish_colors[]')
        service_ids, colors = _normalize_services(raw_service_ids, raw_colors)
        price_map, total_amount, total_minutes = _services_price_amount_and_minutes(service_ids)

        # Compute end_time from start + sum(duration_minutes) 
        start_dt  = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        minutes   = total_minutes
        end_time  = (start_dt + timedelta(minutes=minutes)).strftime("%H:%M:%S")

        # Apply updates
        appt.appointment_date = appointment_date
        appt.start_time       = start_time
        appt.end_time         = end_time
        appt.notes            = notes
        appt.total_amount     = total_amount
        appt.status           = status

        appt.save()

        # Replace APPOINTMENT_SERVICE rows
        with connection.cursor() as c:
            c.execute(
                "DELETE FROM APPOINTMENT_SERVICE WHERE appointment_id = %s",
                [appt.appointment_id]
            )
            for idx, sid in enumerate(service_ids):
                c.execute(
                    """
                    INSERT INTO APPOINTMENT_SERVICE
                      (appointment_id, service_id, service_price, polish_color)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [appt.appointment_id, sid, price_map.get(sid, 0), colors[idx]]
                )

        messages.success(request, 'Appointment updated.')
        return redirect('appointment_list')

    current_services = _load_appointment_service_rows(appt.appointment_id)
    normalized       = _norm_hms_str(appt.start_time)
    slot_values      = [t for (t, _) in time_slots]
    selected_time    = normalized if normalized in slot_values else ""

    return render(request, 'appointments/appointment_edit.html', {
        'appt': appt,
        'staff_opts': staff_opts,
        'cust_opts': cust_opts,
        'svc_opts': svc_opts,
        'current_services': current_services,
        'time_slots': time_slots,
        'selected_time': selected_time,
        'status_choices': STATUS_CHOICES,
    })

# ---------- finish appointment ----------

@transaction.atomic
def appointment_finish(request, appointment_id):
    # Load appointment and basic context for display
    appt = get_object_or_404(Appointment, pk=appointment_id)
    cust = None
    loyalty_points = 0
    if appt:
        custid = appt.customer_id
        cust = get_object_or_404(Customer, pk=custid) if custid else None
        loyalty_points = cust.loyalty_points if cust else 0

    # Only allow finishing scheduled appts
    if (appt.status or '').lower() != 'scheduled':
        messages.error(request, 'Only scheduled appointments can be finished.')
        return redirect('appointment_list')

    # Compute the base amount
    amount = appt.total_amount
    if amount in (None, ''):
        amount = _calc_total_from_services(appt.appointment_id)

    with connection.cursor() as c:
        c.execute("""
            SELECT CONCAT(c.first_name,' ',c.last_name) AS customer_name,
                   CONCAT(s.first_name,' ',s.last_name) AS staff_name
            FROM APPOINTMENT a
            JOIN CUSTOMER c ON a.customer_id = c.customer_id
            JOIN STAFF s ON a.staff_id = s.staff_id
            WHERE a.appointment_id = %s
        """, [appt.appointment_id])
        row = c.fetchone()
    customer_name = row[0] if row else '-'
    staff_name    = row[1] if row else '-'

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', '').strip()
        tip_amount     = request.POST.get('tip_amount') or 0
        transaction_id = request.POST.get('transaction_id', '').strip() or None

       
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return render(request, 'appointments/appointment_finish.html', {
                'appt': appt,
                'customer_name': customer_name,
                'staff_name': staff_name,
                'amount': amount,
            })

        # Create payment
        Payment.objects.create(
            appointment_id=appt.appointment_id,
            payment_method=payment_method,
            amount=amount,
            tip_amount=tip_amount,
            transaction_id=transaction_id,
            payment_date=timezone.now(),
        )

        # Loyalty points updating
        try:
            total_for_points = float(amount or 0) + float(tip_amount or 0)
        except (TypeError, ValueError):
            total_for_points = 0.0

        earned_points = int(total_for_points)  

        cust.loyalty_points = (cust.loyalty_points or 0) + earned_points
        cust.save(update_fields=['loyalty_points'])


        # Mark appointment completed
        appt.status = 'completed'
        appt.save(update_fields=['status'])

        messages.success(request, 'Appointment finished and payment recorded.')
        return redirect('appointment_list')

    # GET — show prefilled payment form
    return render(request, 'appointments/appointment_finish.html', {
        'appt': appt,
        'customer_name': customer_name,
        'staff_name': staff_name,
        'amount': amount,
    })

# ---------- delete ----------

def appointment_delete(request, appointment_id):
    if request.method == 'POST':
        with connection.cursor() as c:
            c.execute("DELETE FROM APPOINTMENT WHERE appointment_id = %s", [appointment_id])
        messages.success(request, 'Appointment deleted.')
        return redirect('appointment_list')
    return redirect('appointment_list')
