# Generated by Django 3.1.7 on 2021-03-15 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0006_auto_20210315_0706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rafflecampaign',
            name='prizes',
        ),
        migrations.AddField(
            model_name='rafflecampaign',
            name='prizes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='draw.prize'),
        ),
    ]