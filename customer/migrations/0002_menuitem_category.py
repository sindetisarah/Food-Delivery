# Generated by Django 3.2.4 on 2021-07-05 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='category',
            field=models.ManyToManyField(related_name='item', to='customer.Category'),
        ),
    ]
