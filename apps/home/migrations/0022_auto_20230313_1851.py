# Generated by Django 3.2.16 on 2023-03-13 12:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20230225_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalledger',
            name='date',
            field=models.DateField(default=datetime.date(2023, 3, 13)),
        ),
        migrations.AlterField(
            model_name='salarybook',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]