# Generated by Django 5.1.6 on 2025-03-04 16:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeapp', '0020_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Failed', 'Failed')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
