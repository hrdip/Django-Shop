# Generated by Django 4.2.10 on 2024-05-09 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('order', '0008_alter_couponmodel_used_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.paymentmodel'),
        ),
    ]
