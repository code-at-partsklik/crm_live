# Generated by Django 5.0.4 on 2024-05-04 08:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_wherehouses_remove_masterproduct_block_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterproduct',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 4, 13, 38, 43, 104238)),
        ),
    ]
