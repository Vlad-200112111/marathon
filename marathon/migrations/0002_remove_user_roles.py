# Generated by Django 4.2.6 on 2023-10-20 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marathon', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
    ]
