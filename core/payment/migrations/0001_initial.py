# Generated by Django 4.2.10 on 2024-05-09 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authority_id', models.CharField(max_length=255)),
                ('ref_id', models.BigIntegerField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('response_json', models.JSONField(default=dict)),
                ('response_code', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'در انتظار پرداخت'), (2, 'پرداخت موفق '), (3, 'پرداخت ناموفق ')], default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
