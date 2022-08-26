# Generated by Django 4.0.6 on 2022-08-26 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_management_system', '0008_delete_searchstring_alter_item_ds_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='item_name',
        ),
        migrations.AddField(
            model_name='item',
            name='free_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='unavailable_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='material',
            name='is_group',
            field=models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=5),
        ),
    ]