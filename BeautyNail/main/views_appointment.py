from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, transaction
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required  # optional; use if you want auth
from datetime import datetime, timedelta, time 
import re

from .models import Appointment  # make sure Appointment model is correct


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
            SELECT service_id, service_name, base_price
            FROM SERVICE
            ORDER BY category, service_name
        """)
        rows = c.fetchall()
    return [{'id': r[0], 'name': r[1], 'price': r[2]} for r in rows]


# ---------- helpers (DRY) ----------

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

def _services_prices_and_total(service_ids):
    """
    Given a list of int service_ids, returns (price_map, total_amount)
    price_map: {service_id -> Decimal}
    total_amount: Decimal | None
    """
    if not service_ids:
        return {}, None
    price_map = _service_price_map(service_ids)
    total_amount = sum(price_map.get(sid, 0) for sid in service_ids) or None
    return price_map, total_amount

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

    # Last resort: if looks like 'HH:MM:SSxxxx', trim to first 8 with padding
    if re.match(r"^\d{2}:\d{2}:\d{2}", s):
        return s[:8]

    return ""


# Consistent time slots used in admin edit template
ADMIN_TIME_SLOTS = [
    ("09:00:00", "9:00 AM"),
    ("10:30:00", "10:30 AM"),
    ("12:00:00", "12:00 PM"),
    ("13:30:00", "1:30 PM"),
    ("15:00:00", "3:00 PM"),
    ("18:30:00", "6:30 PM"),
]


# ---------- list ----------

def appointment_list(request):
    with connection.cursor() as c:
        c.execute("""
            SELECT a.appointment_id, a.appointment_date, a.start_time, a.end_time,
                   a.status, a.total_amount,
                   CONCAT(c.first_name,' ',c.last_name) AS customer_name,
                   CONCAT(s.first_name,' ',s.last_name) AS staff_name
            FROM APPOINTMENT a, CUSTOMER c, STAFF s
            WHERE a.customer_id = c.customer_id
              AND a.staff_id = s.staff_id
            ORDER BY a.appointment_date DESC, a.start_time DESC, a.appointment_id DESC
        """)
        rows = c.fetchall()
    appts = [{
        'id': r[0], 'date': r[1], 'start': r[2], 'end': r[3],
        'status': r[4], 'total': r[5], 'customer': r[6], 'staff': r[7]
    } for r in rows]
    return render(request, 'appointments/appointments.html', {'appointments': appts})


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
        # allow explicit override, else auto-calc +90m
        end_time = (request.POST.get('end_time') or '').strip() or None
        status = (request.POST.get('status') or 'scheduled').strip() or 'scheduled'
        notes = request.POST.get('notes', '').strip() or None

        raw_service_ids = request.POST.getlist('service_ids[]')
        raw_colors = request.POST.getlist('polish_colors[]')
        service_ids, polish_colors = _normalize_services(raw_service_ids, raw_colors)
        price_map, total_amount = _services_prices_and_total(service_ids)

        # basic validation for date & start_time (the grid fills these)
        if not appointment_date or not start_time:
            messages.error(request, "Please pick a date and a time.")
            return render(request, 'appointments/appointment_add.html', {
                'staff_opts': staff_opts,
                'cust_opts': cust_opts,
                'svc_opts': svc_opts,
            })

        # auto-calc end_time if missing (+90 min)
        if not end_time:
            start_dt = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S")
            end_time = (start_dt + timedelta(minutes=90)).strftime("%H:%M:%S")

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
    })


# ---------- edit ----------

from datetime import datetime, timedelta
from django.db import transaction, connection
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@transaction.atomic
def appointment_edit(request, appointment_id):
    appt = get_object_or_404(Appointment, pk=appointment_id)

    staff_opts = _staff_options()
    cust_opts  = _customer_options()
    svc_opts   = _service_options()

    # Same time slots as user flow
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
            })

        # Compute end_time same as user (+90 mins)
        start_dt  = datetime.strptime(f"{appointment_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        end_time  = (start_dt + timedelta(minutes=90)).strftime("%H:%M:%S")

        # Services + total
        raw_service_ids = request.POST.getlist('service_ids[]')
        raw_colors      = request.POST.getlist('polish_colors[]')
        service_ids, colors = _normalize_services(raw_service_ids, raw_colors)
        price_map, total_amount = _services_prices_and_total(service_ids)

        # Apply updates
        appt.appointment_date = appointment_date
        appt.start_time       = start_time
        appt.end_time         = end_time
        appt.notes            = notes
        appt.total_amount     = total_amount
        appt.status           = status  # keep whatever admin chooses

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

    # GET — preselect like user page
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
    })



# ---------- delete ----------

def appointment_delete(request, appointment_id):
    if request.method == 'POST':
        with connection.cursor() as c:
            c.execute("DELETE FROM APPOINTMENT WHERE appointment_id = %s", [appointment_id])
        messages.success(request, 'Appointment deleted.')
        return redirect('appointment_list')
    return redirect('appointment_list')
