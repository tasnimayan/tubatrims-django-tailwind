# Generated by Django 3.2.16 on 2023-02-20 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20230220_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalledger',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
