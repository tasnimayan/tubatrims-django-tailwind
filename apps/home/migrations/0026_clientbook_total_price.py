# Generated by Django 3.2.16 on 2023-04-19 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_alter_clientbook_unit_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientbook',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]
