# Generated by Django 5.1.5 on 2025-01-28 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeapp', '0014_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(related_name='products', to='shoeapp.size'),
        ),
    ]
