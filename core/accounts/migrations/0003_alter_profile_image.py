# Generated by Django 4.2.10 on 2024-05-03 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile/default.png', upload_to='profile/'),
        ),
    ]
