# Generated by Django 3.2.16 on 2023-02-14 19:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20230214_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='g_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='g_phone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='generalledger',
            name='received',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='clientbook',
            name='bill',
            field=models.IntegerField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='clientbook',
            name='client_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.client'),
        ),
        migrations.AlterField(
            model_name='clientbook',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='clientbook',
            name='payment',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='generalledger',
            name='spending',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='generalledger',
            name='user_id',
            field=models.CharField(default='admin', max_length=20),
        ),
        migrations.AlterField(
            model_name='salarybook',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='salarybook',
            name='emp_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.employee'),
        ),
        migrations.AlterField(
            model_name='salarybook',
            name='withdraw',
            field=models.IntegerField(),
        ),
    ]
