# Generated by Django 3.1.7 on 2021-03-15 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0008_auto_20210315_0815'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpcomingRaffleCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='draw.rafflecampaign')),
            ],
            options={
                'verbose_name_plural': 'Upcoming Raffle Campaign',
            },
        ),
    ]
