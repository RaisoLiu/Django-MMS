import json
import random
import string

import numpy as np
import openpyxl
import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .filters import *
from .models import *
from .forms import *


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def material_search(request):
    qs = Item.objects.all()
    itemFilter = ItemFilterTermFreq(request.GET, queryset=qs)
    qs = itemFilter.qs
    n = min(len(qs), 15)
    # qs = qs[:n]
    context = {'item_set': qs, 'itemFilter': itemFilter}
    return render(request, 'material_search.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_item(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'delete_item.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def item_detail(request, pk):
    item = Item.objects.get(id=pk)
    material_set = item.material_set.all()
    context = {'material_set': material_set, 'item': item}
    return render(request, 'item_detail.html', context)


@login_required(login_url='login')
def remaining_material(request):
    return render(request, 'non_development.html')


@login_required(login_url='login')
def project_search(request):
    qs = Project.objects.all()
    n = min(len(qs), 15)
    qs = qs[:n]
    context = {'project_set': qs}
    return render(request, 'project_search.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def new_bom(request, pk):
    project = Project.objects.get(id=pk)
    info = str()
    if request.method == 'POST':
        print(request.POST, request.FILES)
        # form = NEWBOMForm(request.POST)
        excel_file = request.FILES["excel_file"]
        d = request.POST["description"]
        # print(d)
        # print(excel_file)
        # print(df)
        # print(len(df))
        df = pd.read_excel(excel_file, skiprows=8, skipfooter=2)
        bom = BOM(project=project, description=d)
        material_list = []
        total_sum = 0.
        error = 0
        for i in range(len(df)):
            ds = df.iloc[i]['PartNumber']
            qu = int(df.iloc[i]['Quantity'])
            p = 0.
            try:
                item = Item.objects.get(ds_number=ds)
                ms = item.material_set.all()
                qnow = 0
                for j in range(len(ms)):
                    print('q now:', qnow)
                    m = ms[j]
                    if qnow >= qu:
                        break
                    u = min(m.count, qu - qnow)
                    qnow += u
                    m.use(u)
                    m.save()
                    p += u * m.unit_price
                    material_list.append([m.id, u])

            except:
                error += 1
            total_sum += p
        project.total_cost += total_sum
        project.save()
        bom.cost = total_sum
        bom.material_list = json.dumps(material_list)
        bom.save()
        print(bom)
        print(bom.material_list)

        return redirect('/project_detail/'+str(pk))

    context = {'info': info}

    return render(request, 'new_bom.html', context)


@login_required(login_url='login')
def material_detail_search(request):
    return render(request, 'non_development.html')


@login_required(login_url='login')
def materials_price(request):
    context = {}
    if request.method == 'POST':
        print(request.POST, request.FILES)
        excel_file = request.FILES["excel_file"]
        df = pd.read_excel(excel_file, skiprows=8, skipfooter=2)
        mat_set = []
        total_sum = 0.
        error = 0
        for i in range(len(df)):
            it = dict()
            itt = df.iloc[i]
            # print(itt)
            it['no'] = itt['#']
            it['lib_ref'] = itt['LibRef']
            it['ds_number'] = itt['PartNumber']
            it['quantity'] = itt['Quantity']
            item = Item()
            it['color'] = 'table-danger'
            it['price'] = 0.0
            try:
                item = Item.objects.get(ds_number=it['ds_number'])
                ms = item.material_set.all()
                for m in ms:
                    it['price'] = max(it['price'], m.unit_price)
                if item.free_count >= it['quantity']:
                    it['color'] = 'table-info'
                else:
                    it['color'] = 'table-warning'
            except:
                error += 1

            it['sum'] = it['price'] * it['quantity']
            total_sum += it['sum']
            mat_set.append(it)

        context["mat_set"] = mat_set
        context["total_sum"] = total_sum
        context["error"] = error
        print(len(context["mat_set"]))
    return render(request, 'materials_price.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('/project_search')

    context = {'item': project}
    return render(request, 'delete_project.html', context)


@login_required(login_url='login')
def project_detail(request, pk):
    project = Project.objects.get(id=pk)
    bom_set = project.bom_set.all()
    context = {'bom_set': bom_set, 'project': project}
    return render(request, 'project_detail.html', context)


def bom_detail(request, pk):
    bom = BOM.objects.get(id=pk)
    material_set_json = json.loads(bom.material_list)
    material_set = []
    for it in material_set_json:
        obj = Material.objects.get(id=it[0])
        mat = {
            "name": str(obj),
            "unit_price": obj.unit_price,
            "use_quantity": it[1],
            "sum": obj.unit_price * it[1],
            "remaining": obj.count,
        }
        material_set.append(mat)
    print(material_set)
    context = {'material_set': material_set, 'bom': bom}

    return render(request, 'bom_detail.html', context)
