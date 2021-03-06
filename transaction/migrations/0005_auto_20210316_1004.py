# Generated by Django 3.1.7 on 2021-03-16 09:04

from django.db import migrations, models
import transaction.validators


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_transaction_generated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(validators=[transaction.validators.validate_transaction_amount]),
        ),
    ]
