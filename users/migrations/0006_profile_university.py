# Generated by Django 3.1.1 on 2020-09-12 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200912_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='university',
            field=models.CharField(default='', max_length=100),
        ),
    ]
