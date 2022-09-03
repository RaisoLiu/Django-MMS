from django.forms import ModelForm
from django import forms
from .models import *


class ItemForm(ModelForm):
    lib_ref = forms.CharField(label="Lib Ref")
    ds_number = forms.CharField(label="DS Number")
    part_number = forms.CharField(label="Part Number")
    location = forms.CharField(label="存放位置")
    expected_count = forms.IntegerField(label="期望庫存")

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['free_count', 'unavailable_count']


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'


class NewGroupMaterialForm(forms.Form):
    count_per_group = forms.IntegerField(label="每組個數")
    group_count = forms.IntegerField(label="進貨組數", max_value=30)
    price_per_unit = forms.FloatField(label="單價")
    #
    # class Meta:
    #     fields = ['count_per_group', 'group_count', 'price_per_unit']


class NewSplitMaterialForm(forms.Form):
    count = forms.IntegerField(label="每組個數")
    price_per_unit = forms.FloatField(label="單價")


class ProjectForm(ModelForm):
    name = forms.CharField(label="專案名稱")
    user_created = forms.CharField(label="PM")

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['total_cost', 'date_created']


class NEWBOMForm(forms.Form):
    description = forms.CharField(max_length=200)

