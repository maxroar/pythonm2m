from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Item
# Create your views here.
def index(request):
    print(request.session['user_id'])
    all_data = Item.objects.get_all_data(request.session['user_id'])
    context = {
        'data': all_data
    }
    print(all_data['favorites'])
    return render(request, 'items/index.html', context)

def display_add_item(request):
    all_data = Item.objects.get_all_data(request.session['user_id'])
    context = {
        'data': all_data
    }
    return render(request, 'items/add_item.html', context)

def add_item_to_fav(request):
    user_id = request.POST['user_id']
    item_id = request.POST['item_id']
    Item.objects.add_to_favorites(item_id, user_id)
    return redirect('items_ns:index')

def create_item(request):
    if len(request.POST['content']) < 3:
        messages.add_message(request, messages.ERROR, 'Items must be at least 3 characters long.')
        return redirect('items_ns:display_add_item')
    Item.objects.create_item(request.POST, request.session['user_id'])
    return redirect('items_ns:index')

def remove_item(request):
    item_id = request.POST['item_id']
    user_id = request.POST['user_id']
    Item.objects.remove_from_fav(item_id, user_id)
    return redirect('items_ns:index')


def view_item(request, item_id):
    items_info = Item.objects.get_item_data(item_id)
    users = Item.objects.get_item_likers(item_id)
    all_data = Item.objects.get_all_data(request.session['user_id'])
    context = {
        'items_data': items_info,
        'users': users,
        'data': all_data
    }
    return render(request, 'items/item.html', context)
def update_item(request, item_id):
    Item.objects.update_item(request.POST, item_id)
    return redirect('/')

def delete_item(request, item_id):
    Item.objects.delete_item(request.POST, item_id)
    return redirect('/')
