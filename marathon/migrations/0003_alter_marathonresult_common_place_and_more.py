# Generated by Django 4.2.6 on 2023-11-09 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marathon', '0002_rename_uiid_runnerandsponsor_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marathonresult',
            name='common_place',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='marathonresult',
            name='place_by_category',
            field=models.IntegerField(default=0),
        ),
    ]
