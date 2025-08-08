from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib import messages
from .models import Inventory 
from django.utils import timezone

def get_inventory_by_search(query):
    sql = "SELECT * FROM INVENTORY "
    params = []
    if query:
        sql += (
            "WHERE product_name LIKE %s "
            "OR brand LIKE %s "
            "OR category LIKE %s "
            "OR color_name LIKE %s "
            "OR supplier_name LIKE %s "
        )
        search = f"%{query}%"
        params = [search] * 5
    sql += "ORDER BY last_updated DESC, product_name ASC "
    return Inventory.objects.raw(sql, params)

def inventory_list(request):
    query = request.GET.get('search', '').strip()
    items = get_inventory_by_search(query)
    return render(request, 'inventory/inventory.html', {
        'items': items,
        'search_query': query,
    })

def inventory_add(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name', '').strip()
        brand = request.POST.get('brand', '').strip() or None
        category = request.POST.get('category', '').strip()
        color_name = request.POST.get('color_name', '').strip() or None
        quantity_in_stock = request.POST.get('quantity_in_stock') or 0
        unit_cost = request.POST.get('unit_cost')
        retail_price = request.POST.get('retail_price') or None
        reorder_level = request.POST.get('reorder_level') or 5
        supplier_name = request.POST.get('supplier_name', '').strip() or None

        Inventory.objects.create(
            product_name=product_name,
            brand=brand,
            category=category,
            color_name=color_name,
            quantity_in_stock=quantity_in_stock,
            unit_cost=unit_cost,
            retail_price=retail_price,
            reorder_level=reorder_level,
            supplier_name=supplier_name,
            last_updated=timezone.now(),
        )
        messages.success(request, 'Inventory item added.')
        return redirect('inventory_list')

    return render(request, 'inventory/inventory_add.html')

def inventory_edit(request, inventory_id):
    item = get_object_or_404(Inventory, pk=inventory_id)

    if request.method == 'POST':
        item.product_name = request.POST.get('product_name', '').strip()
        item.brand = request.POST.get('brand', '').strip() or None
        item.category = request.POST.get('category', '').strip()
        item.color_name = request.POST.get('color_name', '').strip() or None
        item.quantity_in_stock = request.POST.get('quantity_in_stock') or 0
        item.unit_cost = request.POST.get('unit_cost')
        item.retail_price = request.POST.get('retail_price') or None
        item.reorder_level = request.POST.get('reorder_level') or 5
        item.supplier_name = request.POST.get('supplier_name', '').strip() or None
        item.last_updated = timezone.now()

        item.save()
        messages.success(request, 'Inventory item updated.')
        return redirect('inventory_list')

    return render(request, 'inventory/inventory_edit.html', {'item': item})

def inventory_delete(request, inventory_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM INVENTORY WHERE inventory_id = %s", [inventory_id])
        messages.success(request, 'Inventory item deleted.')
        return redirect('inventory_list')
    return redirect('inventory_list')
