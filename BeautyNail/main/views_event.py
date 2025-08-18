# main/view_events.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib import messages
import os, uuid, imghdr, shutil
from django.conf import settings
from .models import Event  # the model above


IMAGES_SUBDIR = os.path.join('images', 'events')  # inside /static

def _save_event_image_to_static(file_obj):
    import os, uuid, imghdr
    from django.conf import settings

    original = getattr(file_obj, 'name', 'upload')
    _, ext = os.path.splitext(original)
    ext = (ext or '.jpg').lower()

    filename = f"{uuid.uuid4().hex}{ext}"
    # ✅ write into the app's static folder:
    static_dir = os.path.join(settings.BASE_DIR, 'main', 'static', IMAGES_SUBDIR)
    os.makedirs(static_dir, exist_ok=True)

    dest_path = os.path.join(static_dir, filename)
    with open(dest_path, 'wb') as out:
        for chunk in file_obj.chunks():
            out.write(chunk)

    if imghdr.what(dest_path) is None:
        os.remove(dest_path)
        raise ValueError("Uploaded file is not a valid image.")

    # store relative path used by {% static %}
    return os.path.join(IMAGES_SUBDIR, filename).replace('\\', '/')

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
        event_name  = request.POST.get('event_name', '').strip()
        description = request.POST.get('description', '').strip() or None
        start_date  = request.POST.get('start_date') or None
        end_date    = request.POST.get('end_date') or None

        image_file = request.FILES.get('image_file')
        if not image_file:
            messages.error(request, 'Please choose an image file.')
            return render(request, 'events/event_add.html')

        try:
            image_path = _save_event_image_to_static(image_file)  # e.g., 'images/events/abc.jpg'
        except Exception as e:
            messages.error(request, f"Image upload failed: {e}")
            return render(request, 'events/event_add.html')

        Event.objects.create(
            event_name=event_name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            image=image_path,  # store relative path
        )
        messages.success(request, 'Event added.')
        return redirect('event_list')

    return render(request, 'events/event_add.html')

def event_edit(request, events_id):
    event = get_object_or_404(Event, pk=events_id)

    if request.method == 'POST':
        event.event_name  = request.POST.get('event_name', '').strip()
        event.description = request.POST.get('description', '').strip() or None
        event.start_date  = request.POST.get('start_date') or None
        event.end_date    = request.POST.get('end_date') or None

        image_file = request.FILES.get('image_file')
        if image_file:
            try:
                event.image = _save_event_image_to_static(image_file)
            except Exception as e:
                messages.error(request, f"Image upload failed: {e}")
                return render(request, 'events/event_edit.html', {'event': event})

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
