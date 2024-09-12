# Generated by Django 4.1 on 2024-03-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('config_type', models.CharField(max_length=20)),
                ('key', models.CharField(default='', max_length=255)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UILabel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('page_name', models.CharField(max_length=255)),
                ('key', models.CharField(default='', max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('display_value', models.CharField(max_length=255)),
            ],
        ),
    ]
