# Generated by Django 4.0.1 on 2022-05-22 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_deposit_cancel_withdrowal_cancel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
