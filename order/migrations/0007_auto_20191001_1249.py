# Generated by Django 2.1 on 2019-10-01 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0005_auto_20190925_1116'),
        ('order', '0006_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupon.Coupon'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='option',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shop.Option'),
        ),
    ]
