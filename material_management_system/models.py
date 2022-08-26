from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200, blank=True)
    user_created = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    STATUS = (
        ('YES', 'YES'),
        ('NO', 'NO'),
    )

    lib_ref = models.CharField(max_length=200, blank=True)
    ds_number = models.CharField(max_length=200,unique=True)
    part_number = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    expected_count = models.IntegerField(null=True)
    feature = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    free_count = models.IntegerField(default=0)
    unavailable_count = models.IntegerField(default=0)
    is_group = models.CharField(max_length=5, choices=STATUS, default='YES')

    def __str__(self):
        return self.lib_ref

    def add_material(self, val):
        self.free_count += val
        return


class Material(models.Model):
    STATUS = (
        ('YES', 'YES'),
        ('NO', 'NO'),
    )
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    random_str = models.CharField(max_length=20)
    unit_price = models.FloatField()
    count = models.IntegerField(default=0)
    is_free = models.CharField(max_length=5, default='YES', choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item) + ' ' + self.random_str


class BOM(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True)
    material = models.ManyToManyField(Material)

    def __str__(self):
        return str(self.project) + str(self.description)
