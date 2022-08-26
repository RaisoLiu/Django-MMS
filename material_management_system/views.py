from django.shortcuts import render, redirect
from .filters import *
from .models import *
from .forms import *


def material_search(request):
    qs = Item.objects.all()
    itemFilter = ItemFilterTermFreq(request.GET, queryset=qs)
    qs = itemFilter.qs
    n = min(len(qs), 10)
    qs = qs[:n]
    context = {'item_set': qs, 'itemFilter': itemFilter}
    return render(request, 'material_search.html', context)


def new_item(request):
    formset = ItemForm()
    info = str()
    if request.method == 'POST':
        formset = ItemForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        else:
            print('data is not valid.')
            info = 'data is not valid.'

    context = {'form': formset, 'info': info}

    return render(request, 'new_item.html', context)


def update_item(request, pk):
    item = Item.objects.get(id=pk)
    formset = ItemForm(instance=item)
    info = str()
    if request.method == 'POST':
        formset = ItemForm(request.POST, instance=item)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        else:
            print('data is not valid.')
            info = 'data is not valid.'

    context = {'form': formset, 'info': info}
    return render(request, 'new_item.html', context)


def delete_item(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'delete.html', context)



def new_material(request, pk):
    return None


def remaining_material(request):
    return None


def project_search(request):
    return None


def new_project(request):
    return None


def new_bom(request):
    return None


def update_material(request):
    return None


def item_detail(request, pk):
    return None