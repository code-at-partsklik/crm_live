# Generated by Django 5.0.4 on 2024-05-04 09:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_alter_masterproduct_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterproduct',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 4, 14, 42, 9, 70449)),
        ),
    ]
