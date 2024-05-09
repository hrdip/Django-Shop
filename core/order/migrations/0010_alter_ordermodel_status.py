# Generated by Django 4.2.10 on 2024-05-09 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_ordermodel_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='status',
            field=models.IntegerField(choices=[(1, 'در انتظار پرداخت'), (2, 'پرداخت با موفقیت انجام شده'), (3, 'لغو شده')], default=1),
        ),
    ]