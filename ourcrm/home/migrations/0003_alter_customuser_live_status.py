# Generated by Django 5.0.4 on 2024-04-30 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_user_status_customuser_user_role_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='live_status',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]