# Generated by Django 4.0.5 on 2023-05-28 19:02

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0002_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=50, null=True),
        ),
    ]
