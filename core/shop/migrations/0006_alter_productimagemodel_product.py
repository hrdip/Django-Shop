# Generated by Django 4.2.10 on 2024-05-04 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_productmodel_brief_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimagemodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='shop.productmodel'),
        ),
    ]
