# Generated by Django 4.2.10 on 2024-04-22 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_productmodel_discount_pecent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='breif_description',
            new_name='brief_description',
        ),
    ]