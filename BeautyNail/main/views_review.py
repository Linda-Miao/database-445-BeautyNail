# reviews/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib import messages
from django.utils import timezone
from .models import Review  # assumes model class Review mapped to REVIEW table

def get_reviews_by_search(query):
    sql = "SELECT * FROM REVIEW "
    params = []
    if query:
        sql += (
            "WHERE CAST(review_id AS CHAR) LIKE %s "
            "OR CAST(customer_id AS CHAR) LIKE %s "
            "OR CAST(appointment_id AS CHAR) LIKE %s "
            "OR CAST(staff_id AS CHAR) LIKE %s "
            "OR CAST(rating AS CHAR) LIKE %s "
            "OR comment LIKE %s "
        )
        search = f"%{query}%"
        params = [search, search, search, search, search, search]
    sql += "ORDER BY review_date DESC, review_id DESC "
    return Review.objects.raw(sql, params)

def reviews_list(request):
    query = request.GET.get('search', '').strip()
    items = get_reviews_by_search(query)
    return render(request, 'reviews/reviews.html', {
        'items': items,
        'search_query': query,
    })

def review_add(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id', '').strip()
        appointment_id = request.POST.get('appointment_id', '').strip()
        staff_id = request.POST.get('staff_id', '').strip()
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip() or None

        Review.objects.create(
            customer_id=customer_id,
            appointment_id=appointment_id,
            staff_id=staff_id,
            rating=rating,
            comment=comment,
            review_date=timezone.now(),
        )
        messages.success(request, 'Review added.')
        return redirect('reviews_list')

    return render(request, 'reviews/review_add.html')

def review_edit(request, review_id):
    item = get_object_or_404(Review, pk=review_id)

    if request.method == 'POST':
        item.customer_id = request.POST.get('customer_id', '').strip()
        item.appointment_id = request.POST.get('appointment_id', '').strip()
        item.staff_id = request.POST.get('staff_id', '').strip()
        item.rating = request.POST.get('rating')
        item.comment = request.POST.get('comment', '').strip() or None
        item.review_date = timezone.now()

        item.save()
        messages.success(request, 'Review updated.')
        return redirect('reviews_list')

    return render(request, 'reviews/review_edit.html', {'item': item})

def review_delete(request, review_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM REVIEW WHERE review_id = %s", [review_id])
        messages.success(request, 'Review deleted.')
        return redirect('reviews_list')
    return redirect('reviews_list')
