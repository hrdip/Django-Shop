# Generated by Django 4.2.10 on 2024-05-06 08:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0006_alter_productimagemodel_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('discount_percent', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('max_limit_usage', models.PositiveIntegerField(default=10)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('used_by', models.ManyToManyField(related_name='coupon_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddresModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=250)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addres', models.CharField(max_length=250)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=50)),
                ('status', models.IntegerField(choices=[(1, 'در انتظار پرداخت'), (2, 'در حال پرداخت'), (3, ' ارسال شده'), (4, 'تحویل داده شده'), (5, 'لغو شده')], default=1)),
                ('total_price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='order.couponmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.ordermodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.productmodel')),
            ],
        ),
    ]
