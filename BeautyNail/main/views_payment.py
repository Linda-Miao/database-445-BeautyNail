# payments/views.py
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib import messages
from django.utils import timezone
from .models import Payment  

def get_payments_by_search(query):
    sql = "SELECT * FROM PAYMENT "
    params = []
    if query:
        sql += (
            "WHERE CAST(appointment_id AS CHAR) LIKE %s "
            "OR payment_method LIKE %s "
            "OR CAST(amount AS CHAR) LIKE %s "
            "OR CAST(tip_amount AS CHAR) LIKE %s "
            "OR transaction_id LIKE %s "
        )
        search = f"%{query}%"
        params = [search] * 5
    sql += "ORDER BY payment_date DESC, payment_id DESC "
    return Payment.objects.raw(sql, params)

def payment_list(request):
    query = request.GET.get('search', '').strip()
    items = get_payments_by_search(query)
    return render(request, 'payments/payments.html', {
        'items': items,
        'search_query': query,
    })

def payment_add(request):
    if request.method == 'POST':
        appointment_id = (request.POST.get('appointment_id') or '').strip()
        payment_method = (request.POST.get('payment_method') or '').strip()
        amount = request.POST.get('amount')
        tip_amount = request.POST.get('tip_amount') or 0
        transaction_id = (request.POST.get('transaction_id') or '').strip() or None

        Payment.objects.create(
            appointment_id=appointment_id,
            payment_method=payment_method,
            amount=amount,
            tip_amount=tip_amount,
            payment_date=timezone.now(),
            transaction_id=transaction_id,
        )

        # ✅ Loyalty points = int(amount + tip_amount)
        try:
            total = float(amount or 0) + float(tip_amount or 0)
        except (TypeError, ValueError):
            total = 0.0
            

        total = int(total)

        if appointment_id and total:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE CUSTOMER c
                    JOIN APPOINTMENT a ON a.customer_id = c.customer_id
                    SET c.loyalty_points = COALESCE(c.loyalty_points, 0)
                                         + CAST(ROUND(%s, 0) AS SIGNED)
                    WHERE a.appointment_id = %s
                    """,
                    [total, appointment_id]
                )

        messages.success(request, 'Payment recorded.')
        return redirect('payment_list')

    return render(request, 'payments/payment_add.html')


def payment_edit(request, payment_id):
    item = get_object_or_404(Payment, pk=payment_id)

    if request.method == 'POST':
        item.appointment_id = request.POST.get('appointment_id', '').strip()
        item.payment_method = request.POST.get('payment_method', '').strip()
        item.amount = request.POST.get('amount')
        item.tip_amount = request.POST.get('tip_amount') or 0
        item.transaction_id = request.POST.get('transaction_id', '').strip() or None
        item.payment_date = timezone.now()

        item.save()
        messages.success(request, 'Payment updated.')
        return redirect('payment_list')

    return render(request, 'payments/payment_edit.html', {'item': item})

def payment_delete(request, payment_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM PAYMENT WHERE payment_id = %s", [payment_id])
        messages.success(request, 'Payment deleted.')
        return redirect('payment_list')
    return redirect('payment_list')
