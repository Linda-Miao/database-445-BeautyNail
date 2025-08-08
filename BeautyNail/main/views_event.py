# main/view_events.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib import messages
from .models import Event  # the model above

def get_events_by_search(query):
    sql = "SELECT * FROM events "
    params = []
    if query:
        sql += (
            "WHERE event_name LIKE %s "
            "OR description LIKE %s "
        )
        search = f"%{query}%"
        params = [search] * 2
    sql += "ORDER BY start_date DESC, end_date DESC "
    return Event.objects.raw(sql, params)

def event_list(request):
    query = request.GET.get('search', '').strip()
    events = get_events_by_search(query)
    return render(request, 'events/events.html', {
        'events': events,
        'search_query': query,
    })

def event_add(request):
    if request.method == 'POST':
        event_name = request.POST.get('event_name', '').strip()
        description = request.POST.get('description', '').strip() or None  
        start_date = request.POST.get('start_date') or None
        end_date = request.POST.get('end_date') or None
        image = request.POST.get('image', '').strip() or None

        Event.objects.create(
            event_name=event_name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            image=image,
        )
        messages.success(request, 'Event added.')
        return redirect('event_list')

    return render(request, 'events/event_add.html')

def event_edit(request, events_id):
    event = get_object_or_404(Event, pk=events_id)

    if request.method == 'POST':
        event.event_name = request.POST.get('event_name', '').strip()
        event.description = request.POST.get('description', '').strip() or None
        event.start_date = request.POST.get('start_date') or None
        event.end_date = request.POST.get('end_date') or None
        event.image = request.POST.get('image', '').strip() or None

        event.save()
        messages.success(request, 'Event updated.')
        return redirect('event_list')

    return render(request, 'events/event_edit.html', {'event': event})

def event_delete(request, events_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM events WHERE events_id = %s", [events_id])
        messages.success(request, 'Event deleted.')
        return redirect('event_list')
    return redirect('event_list')
