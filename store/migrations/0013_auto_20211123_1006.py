# Generated by Django 3.2.8 on 2021-11-23 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20211122_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
