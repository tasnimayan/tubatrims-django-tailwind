# Generated by Django 3.2.16 on 2023-02-12 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20230212_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.AutoField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
