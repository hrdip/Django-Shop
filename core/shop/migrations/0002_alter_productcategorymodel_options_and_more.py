# Generated by Django 4.2.10 on 2024-04-22 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategorymodel',
            options={'ordering': ['-created_date']},
        ),
        migrations.AlterModelOptions(
            name='productmodel',
            options={'ordering': ['-created_date']},
        ),
        migrations.RenameField(
            model_name='productimagemodel',
            old_name='files',
            new_name='file',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='breif_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]