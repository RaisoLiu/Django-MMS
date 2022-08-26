from django.forms import ModelForm
from django import forms
from .models import *


class ItemForm(ModelForm):
    # lib_ref = forms.CharField(label="Lib Ref")
    # ds_number = forms.CharField(label="DS Number")
    # part_number = forms.CharField(label="Part Number")
    # location = forms.CharField(label="存放位置")
    # expected_count = forms.CharField(label="期望庫存")
    # feature = forms.CharField(label="Features")

    class Meta:
        model = Item
        fields = '__all__'