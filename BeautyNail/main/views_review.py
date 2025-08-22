# reviews/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Review, Customer  


def get_reviews_by_search(query):
    sql = """
        SELECT
          r.review_id,                         
          r.review_id AS id,                   
          r.appointment_id,
          r.rating,
          r.comment,
          r.review_date,
          CONCAT(c.first_name,' ',c.last_name) AS customer_name,
          CONCAT(s.first_name,' ',s.last_name) AS staff_name
        FROM REVIEW r
        JOIN CUSTOMER c ON r.customer_id = c.customer_id
        JOIN STAFF s    ON r.staff_id    = s.staff_id
    """
    params = []
    if query:
        sql += """
        WHERE
            CONCAT(c.first_name,' ',c.last_name) LIKE %s OR
            CONCAT(s.first_name,' ',s.last_name) LIKE %s OR
            CAST(r.appointment_id AS CHAR) LIKE %s OR
            CAST(r.rating AS CHAR) LIKE %s OR
            r.comment LIKE %s
        """
        s = f"%{query}%"
        params = [s, s, s, s, s]

    sql += " ORDER BY r.review_date DESC, r.review_id DESC "
    return Review.objects.raw(sql, params)

@login_required
def reviews_list(request):
    query = request.GET.get('search', '').strip()
    items = get_reviews_by_search(query)
    return render(request, 'reviews/reviews.html', {
        'items': items,
        'search_query': query,
    })

@login_required
def review_delete(request, review_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM REVIEW WHERE review_id = %s", [review_id])
        messages.success(request, 'Review deleted.')
        return redirect('reviews_list')
    return redirect('reviews_list')

@login_required
def my_review_delete(request, review_id):
    customer = get_object_or_404(Customer, user_id=request.user.id)
    review = get_object_or_404(Review, pk=review_id, customer_id=customer.customer_id)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted.')
    return redirect('my_appointments')
