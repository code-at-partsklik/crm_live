# Generated by Django 5.0.4 on 2024-05-04 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_masterproduct_mrp_alter_masterproduct_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterproduct',
            name='gst_percent',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='masterproduct',
            name='hsn_code',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
