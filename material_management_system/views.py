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
    n = min(len(qs), 15)
    # qs = qs[:n]
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
    return render(request, 'delete_item.html', context)


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
                'count': n,
                'unit_price': p,
            }
            for i in range(g):
                material_dict['random_str'] = ''.join(random.choice(string.ascii_uppercase) for x in range(6))
                material = Material(**material_dict)
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
            material = Material(**material_dict)
            material.save()
            item.save()
        return redirect('/')

    form = NewGroupMaterialForm() if is_group else NewSplitMaterialForm()
    context = {'item': item, 'form': form, 'info': info}
    return render(request, 'new_material.html', context)


def update_material(request, pk):
    material = Material.objects.get(id=pk)
    item = material.item
    form = MaterialForm(instance=material)
    info = str()
    if request.method == 'POST':
        ori = material.count
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            item.add_material(Material.objects.get(id=pk).count - ori)
            item.save()
            return redirect('/item_detail/' + str(item.id))

        else:
            print('data is not valid.')
            info = 'data is not valid.'

    context = {'form': form, 'info': info}
    return render(request, 'update_material.html', context)


def delete_material(request, pk):
    material = Material.objects.get(id=pk)
    item = material.item
    if request.method == "POST":
        item.add_material(-material.count)
        item.save()
        material.delete()
        return redirect('/item_detail/' + str(item.id))

    context = {'material': material, 'item': item}
    return render(request, 'delete_material.html', context)


def item_detail(request, pk):
    item = Item.objects.get(id=pk)
    material_set = item.material_set.all()
    context = {'material_set': material_set, 'item': item}
    return render(request, 'item_detail.html', context)


def remaining_material(request):
    return render(request, 'non_development.html')


def project_search(request):
    qs = Project.objects.all()
    n = min(len(qs), 15)
    qs = qs[:n]
    context = {'project_set': qs}
    return render(request, 'project_search.html', context)


def new_project(request):
    project_form = ProjectForm()
    info = str()
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            return redirect('/project_search')
        else:
            print('data is not valid.')
            info = 'data is not valid.'

    context = {'form': project_form, 'info': info}

    return render(request, 'new_project.html', context)


def new_bom(request, pk):
    project = Project.objects.get(id=pk)
    bom_form = BOMForm(initial={'project': project})
    info = str()
    if request.method == 'POST':
        bom_form = BOMForm(request.POST)
        if bom_form.is_valid():
            bom_form.save()
            return redirect('/project_detail/'+str(pk))
        else:
            print('data is not valid.')
            info = 'data is not valid.'

    context = {'form': bom_form, 'info': info}

    return render(request, 'new_bom.html', context)


def material_detail_search(request):
    return render(request, 'non_development.html')


def materials_price(request):
    return render(request, 'non_development.html')


def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    info = str()
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('/project_search')
        else:
            print('data is not valid.')
            info = 'data is not valid.'

    context = {'form': form, 'info': info}
    return render(request, 'new_project.html', context)


def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('/project_search')

    context = {'item': project}
    return render(request, 'delete_project.html', context)


def project_detail(request, pk):
    project = Project.objects.get(id=pk)
    bom_set = project.bom_set.all()
    context = {'bom_set': bom_set, 'project': project}
    return render(request, 'project_detail.html', context)
