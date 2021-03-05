# Generated by Django 3.1.7 on 2021-03-04 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.CharField(blank=True, max_length=50, verbose_name='Department'),
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='profile',
            name='room_no',
            field=models.CharField(blank=True, max_length=20, verbose_name='Room Number'),
        ),
    ]