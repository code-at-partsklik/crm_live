# Generated by Django 5.0.4 on 2024-05-02 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_productbrand_producttype_masterproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterproduct',
            name='mrp',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='masterproduct',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
