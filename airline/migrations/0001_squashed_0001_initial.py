# Generated by Django 5.1 on 2024-08-08 17:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('airline', '0001_initial')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('callsign', models.CharField(max_length=50)),
                ('founded_year', models.IntegerField(validators=[django.core.validators.MaxValueValidator(2024), django.core.validators.MinValueValidator(1800)])),
                ('base_airport', models.CharField(max_length=50)),
            ],
        ),
    ]
