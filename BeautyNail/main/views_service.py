from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib import messages
from .models import Service 

def get_services_by_search(query):
    sql = "SELECT * FROM SERVICE "
    params = []
    if query:
        sql += (
            "WHERE service_name LIKE %s "
            "OR description LIKE %s "
            "OR category LIKE %s "
        )
        search = f"%{query}%"
        params = [search, search, search]
    sql += "ORDER BY category ASC, service_name ASC "
    return Service.objects.raw(sql, params)

def get_top_services():
    sql = """
        SELECT
            s.*,
            COUNT(asv.service_id) AS usage_count,
            (COUNT(asv.service_id) * s.base_price) AS total_benefit
        FROM SERVICE s
        JOIN APPOINTMENT_SERVICE asv
          ON asv.service_id = s.service_id
        GROUP BY s.service_id
        ORDER BY total_benefit DESC
        LIMIT 5
    """
    return Service.objects.raw(sql)

def service_list(request):
    query = request.GET.get('search', '').strip()
    top = request.GET.get('top_services')
    if top:
        services = get_top_services()
    else:
        services = get_services_by_search(query)
    return render(request, 'services/services.html', {
        'services': services,
        'search_query': query,
    })

def service_add(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name', '').strip()
        description = request.POST.get('description', '').strip() or None
        base_price = request.POST.get('base_price')
        duration_minutes = request.POST.get('duration_minutes') or 0
        category = request.POST.get('category', '').strip()
        requies_appointment = request.POST.get('requies_appointment', '1')  
        requies_appointment = 1 if str(requies_appointment) == '1' else 0

        Service.objects.create(
            service_name=service_name,
            description=description,
            base_price=base_price,
            duration_minutes=duration_minutes,
            category=category,
            requies_appointment=requies_appointment,
        )
        messages.success(request, 'Service added.')
        return redirect('service_list')

    return render(request, 'services/service_add.html')

def service_edit(request, service_id):
    svc = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        svc.service_name = request.POST.get('service_name', '').strip()
        svc.description = request.POST.get('description', '').strip() or None
        svc.base_price = request.POST.get('base_price')
        svc.duration_minutes = request.POST.get('duration_minutes') or 0
        svc.category = request.POST.get('category', '').strip()
        rq = request.POST.get('requies_appointment', '1')
        svc.requies_appointment = 1 if str(rq) == '1' else 0

        svc.save()
        messages.success(request, 'Service updated.')
        return redirect('service_list')

    return render(request, 'services/service_edit.html', {'svc': svc})

def service_delete(request, service_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM SERVICE WHERE service_id = %s", [service_id])
        messages.success(request, 'Service deleted.')
        return redirect('service_list')
    return redirect('service_list')
