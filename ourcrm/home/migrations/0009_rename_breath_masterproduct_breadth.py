# Generated by Django 5.0.4 on 2024-05-02 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_masterproduct_mrp_alter_masterproduct_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='masterproduct',
            old_name='breath',
            new_name='breadth',
        ),
    ]
