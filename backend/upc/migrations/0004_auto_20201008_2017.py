# Generated by Django 3.1.2 on 2020-10-08 20:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('upc', '0003_auto_20201008_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
