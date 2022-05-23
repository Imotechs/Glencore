# Generated by Django 4.0.1 on 2022-05-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_account_balance_alter_deposit_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrowal',
            name='wallet_address',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='withdrowal',
            name='amount',
            field=models.FloatField(verbose_name='USD'),
        ),
        migrations.AlterField(
            model_name='withdrowal',
            name='date_approved',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='withdrowal',
            name='date_placed',
            field=models.DateTimeField(blank=True),
        ),
    ]
