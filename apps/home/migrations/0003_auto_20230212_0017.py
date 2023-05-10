# Generated by Django 3.2.16 on 2023-02-11 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20230211_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateAttendance',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='generalledger',
            name='user_id',
            field=models.CharField(default='ADMIN', max_length=20),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.dateattendance')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.employee')),
            ],
            options={
                'unique_together': {('employee', 'date')},
            },
        ),
    ]
