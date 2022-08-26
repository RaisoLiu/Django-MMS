from .models import *

material_list = Material.objects.all()

for it in material_list:
    it.delete()

item_list = Item.objects.all()

for it in item_list:
    it.free_count = 0
    it.unavailable_count = 0
    it.save()
