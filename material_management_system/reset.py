import os
import random
import string

from material_management_system.models import *
import pandas as pd
import numpy as np

model_list = ['Material', 'Item', 'Project', 'BOM']

for it in model_list:
    li = locals()[it].objects.all()
    for itt in li:
        itt.delete()

BASE_DIR = os.getcwd()
EXCEL_DIR = os.path.join(BASE_DIR, 'material_management_system', 'excel')

excel = 'CAP.xlsx'

lib_ref_col = "LibRef"
ds_number_col = "料號"
part_number_col = "料號"
count_col = "庫存數量"
price_col = "單顆單價(NT)"

feature_list = ["電容值 (F)", "包裝", "耐壓(V)", "誤差 (%)", "材質", "廠牌"]

# ADD ITEM
path = os.path.join(EXCEL_DIR, excel)
page_list = pd.ExcelFile(path).sheet_names
for page in range(len(page_list)):
    df = pd.read_excel(path, sheet_name=page)
    print(page, df.shape)
    lib_ref_li = np.array(df[lib_ref_col])
    ds_number_li = np.array(df[ds_number_col])
    count_li = np.array(df[count_col])
    price_li = np.array(df[price_col])
    feature_li = np.array(df[feature_list], dtype=str)
    n = len(lib_ref_li)
    m = feature_li.shape[1]
    for i in range(n):
        feature_str = ""
        for j in range(m):
            feature_str += feature_list[j] + ' '
            feature_str += feature_li[i][j] + ', '
        item_dict = {
            'lib_ref': lib_ref_li[i],
            'ds_number': ds_number_li[i],
            'part_number': ds_number_li[i],
            'feature': feature_str
        }
        if len(str(ds_number_li[i])) < 10:
            continue
        if len(str(item_dict['lib_ref'])) < 10:
            item_dict['lib_ref'] = item_dict['ds_number']
        if len(str(item_dict['ds_number'])) < 10:
            item_dict['ds_number'] = item_dict['lib_ref']

        if len(str(ds_number_li[i])) < 10:
            continue
        item = Item(**item_dict)
        try:
            item.save()
        except:
            pass

        item = Item.objects.get(ds_number=item_dict['ds_number'])
        p = 0.0
        try:
            p = float(price_li[i])
        except:
            pass
        if np.isnan(p):
            p = 0.0
        c = 0
        try:
            c = int(count_li[i])
        except:
            continue
        if c == 0:
            continue
        material_dict = {
            'item': item,
            'random_str': ''.join(random.choice(string.ascii_uppercase) for x in range(6)),
            'count': c,
            'unit_price': p,
        }
        material = Material(**material_dict)
        material.save()
        item.add_material(c)
        item.save()

excel = 'RES.xlsx'

lib_ref_col = "LibRef"
ds_number_col = "料號"
part_number_col = "料號"

feature_list = ["電阻值 (W)", "包裝", "誤差(%)", "廠牌"]

# ADD ITEM
path = os.path.join(EXCEL_DIR, excel)
page_list = pd.ExcelFile(path).sheet_names
for page in range(len(page_list)):
    df = pd.read_excel(path, sheet_name=page)
    print(page, df.shape)
    lib_ref_li = np.array(df[lib_ref_col])
    ds_number_li = np.array(df[ds_number_col])
    feature_li = np.array(df[feature_list], dtype=str)
    n = len(lib_ref_li)
    m = feature_li.shape[1]
    for i in range(n):
        feature_str = ""
        for j in range(m):
            feature_str += feature_list[j] + ' '
            feature_str += feature_li[i][j] + ', '
        item_dict = {
            'lib_ref': lib_ref_li[i],
            'ds_number': ds_number_li[i],
            'part_number': ds_number_li[i],
            'feature': feature_str
        }
        if len(str(ds_number_li[i])) < 10:
            continue
        item = Item(**item_dict)
        try:
            item.save()
        except:
            pass

        item = Item.objects.get(ds_number=item_dict['ds_number'])
        p = 0.0
        try:
            p = float(price_li[i])
        except:
            pass
        if np.isnan(p):
            p = 0.0
        c = 0
        try:
            c = int(count_li[i])
        except:
            continue
        if c == 0:
            continue
        material_dict = {
            'item': item,
            'random_str': ''.join(random.choice(string.ascii_uppercase) for x in range(6)),
            'count': c,
            'unit_price': p,
        }
        material = Material(**material_dict)
        material.save()
        item.add_material(c)
        item.save()

excel = 'IC.xlsx'

lib_ref_col = "LibRef"
ds_number_col = "料號"
part_number_col = "料號"

feature_list = ["廠牌"]

# ADD ITEM
path = os.path.join(EXCEL_DIR, excel)
page_list = pd.ExcelFile(path).sheet_names
for page in range(len(page_list)):
    df = pd.read_excel(path, sheet_name=page)
    print(page, df.shape)
    lib_ref_li = np.array(df[lib_ref_col])
    ds_number_li = np.array(df[ds_number_col])
    feature_li = np.array(df[feature_list], dtype=str)
    n = len(lib_ref_li)
    m = feature_li.shape[1]
    for i in range(n):
        feature_str = ""
        for j in range(m):
            feature_str += feature_list[j] + ' '
            feature_str += feature_li[i][j] + ', '
        item_dict = {
            'lib_ref': lib_ref_li[i],
            'ds_number': ds_number_li[i],
            'part_number': ds_number_li[i],
            'feature': feature_str
        }
        if len(str(item_dict['lib_ref'])) < 10:
            item_dict['lib_ref'] = item_dict['ds_number']
        if len(str(ds_number_li[i])) < 10:
            continue
        item = Item(**item_dict)
        try:
            item.save()
        except:
            pass

        item = Item.objects.get(ds_number=item_dict['ds_number'])
        p = 0.0
        try:
            p = float(price_li[i])
        except:
            pass
        if np.isnan(p):
            p = 0.0
        c = 0
        try:
            c = int(count_li[i])
        except:
            continue
        if c == 0:
            continue
        material_dict = {
            'item': item,
            'random_str': ''.join(random.choice(string.ascii_uppercase) for x in range(6)),
            'count': c,
            'unit_price': p,
        }
        material = Material(**material_dict)
        material.save()
        item.add_material(c)
        item.save()

excel = 'DIO.xlsx'

lib_ref_col = "LibRef"
ds_number_col = "料號"
part_number_col = "料號"
count_col = "庫存數量"
price_col = "單顆單價(NT)"

feature_list = ["廠牌"]

# ADD ITEM
path = os.path.join(EXCEL_DIR, excel)
page_list = pd.ExcelFile(path).sheet_names
for page in range(len(page_list)):
    df = pd.read_excel(path, sheet_name=page)
    print(page, df.shape)
    lib_ref_li = np.array(df[lib_ref_col])
    count_li = np.array(df[count_col])
    price_li = np.array(df[price_col])
    ds_number_li = np.array(df[ds_number_col])
    feature_li = np.array(df[feature_list], dtype=str)
    n = len(lib_ref_li)
    m = feature_li.shape[1]
    for i in range(n):
        feature_str = ""
        for j in range(m):
            feature_str += feature_list[j] + ' '
            feature_str += feature_li[i][j] + ', '
        item_dict = {
            'lib_ref': lib_ref_li[i],
            'ds_number': ds_number_li[i],
            'part_number': ds_number_li[i],
            'feature': feature_str
        }
        if len(str(item_dict['lib_ref'])) < 10:
            item_dict['lib_ref'] = item_dict['ds_number']
        if len(str(ds_number_li[i])) < 10:
            continue
        item = Item(**item_dict)
        try:
            item.save()
        except:
            pass

        item = Item.objects.get(ds_number=item_dict['ds_number'])
        p = 0.0
        try:
            p = float(price_li[i])
        except:
            pass
        if np.isnan(p):
            p = 0.0
        c = 0
        try:
            c = int(count_li[i])
        except:
            continue
        if c == 0:
            continue
        material_dict = {
            'item': item,
            'random_str': ''.join(random.choice(string.ascii_uppercase) for x in range(6)),
            'count': c,
            'unit_price': p,
        }
        material = Material(**material_dict)
        material.save()
        item.add_material(c)
        item.save()

project = Project(name="P1", description="D1", user_created="PM1")
project.save()
