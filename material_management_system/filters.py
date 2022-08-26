import django_filters
from django_filters import CharFilter

from .models import *


class ItemFilter(django_filters.FilterSet):
    feature = CharFilter(field_name='feature', lookup_expr='icontains')

    # feature = CharFilter(method='multi_field')

    class Meta:
        model = Item
        fields = []

    # def multi_field(self, qs, name, value):
    #     return qs.filter(Item(lib_ref=value) | Item(feature=value) | Item(part_number=value) | Item(ds_number=value))


class ItemFilterTermFreq(django_filters.FilterSet):
    feature = CharFilter(method='multi_field')

    def multi_field(self, qs, name, value):
        cf_feature = CharFilter(field_name='feature', lookup_expr='icontains')
        cf_lib_ref = CharFilter(field_name='lib_ref', lookup_expr='icontains')
        cf_part_number = CharFilter(field_name='part_number', lookup_expr='icontains')
        cf_ds_number = CharFilter(field_name='ds_number', lookup_expr='icontains')
        return (cf_lib_ref.filter(qs, value=value) |
                cf_part_number.filter(qs, value=value) |
                cf_ds_number.filter(qs, value=value) |
                cf_feature.filter(qs, value=value))

    class Meta:
        model = Item
        fields = []
