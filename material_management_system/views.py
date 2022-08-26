import random
import string

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
    form = ItemForm(instance=item)
    info = str()
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print('data is not valid.')
            info = 'data is not valid.'

    context = {'form': form, 'info': info}
    return render(request, 'new_item.html', context)


def delete_item(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'delete.html', context)


def new_material(request, pk):
    item = Item.objects.get(id=pk)
    is_group = 1 if item.is_group == 'YES' else 0
    info = ""
    if request.method == 'POST':
        form = NewGroupMaterialForm(request.POST) if is_group else NewSplitMaterialForm(request.POST)
        if is_group:
            n = int(form['count_per_group'].value())
            g = int(form['group_count'].value())
            p = float(form['price_per_unit'].value())
            item.add_material(n * g)
            material_dict = {
                'item': item,
                'count': g,
                'unit_price': p,
            }
            for i in range(n):
                material_dict['random_str'] = ''.join(random.choice(string.ascii_uppercase) for x in range(6))
                material = MaterialForm(initial=material_dict)
                if material.is_valid():
                    material.save()
            item.save()
        else:
            n = int(form['count'].value())
            p = float(form['price_per_unit'].value())
            item.add_material(n)
            material_dict = {
                'item': item,
                'random_str': ''.join(random.choice(string.ascii_uppercase) for x in range(6)),
                'count': n,
                'unit_price': p,
            }
            material = MaterialForm(initial=material_dict)
            if material.is_valid():
                material.save()
            item.save()
        return redirect('/')

    form = NewGroupMaterialForm() if is_group else NewSplitMaterialForm()
    context = {'item': item, 'form': form, 'info': info}
    return render(request, 'new_material.html', context)


def remaining_material(request):
    return render(request, 'non_development.html')


def project_search(request):
    return render(request, 'non_development.html')


def new_project(request):
    return render(request, 'non_development.html')


def new_bom(request):
    return render(request, 'non_development.html')


def update_material(request):
    return render(request, 'non_development.html')


def item_detail(request, pk):
    return render(request, 'non_development.html')
