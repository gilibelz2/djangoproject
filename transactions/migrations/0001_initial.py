# Generated by Django 3.0.8 on 2020-07-25 20:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PolicyRule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0)),
                ('destinations', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), size=None)),
                ('currency', models.CharField(blank=True, choices=[('BTC', 'Bitcoin'), ('USD', 'United States Dollar')], default='BTC', max_length=3)),
                ('amount_in_satoshis', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('destination', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('O', 'Outgoing'), ('R', 'Rejected')], default='R', max_length=1)),
            ],
        ),
    ]