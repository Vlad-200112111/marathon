# Generated by Django 4.2.6 on 2023-11-10 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marathon', '0004_remove_marathonresult_charitable_organization_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='runnerandsponsor',
            name='charitable_organization',
        ),
        migrations.AddField(
            model_name='runner',
            name='charitable_organization',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='marathon.charitableorganization'),
        ),
    ]