# Generated by Django 3.1.7 on 2021-03-15 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0007_auto_20210315_0814'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rafflecampaign',
            old_name='prizes',
            new_name='prize',
        ),
    ]