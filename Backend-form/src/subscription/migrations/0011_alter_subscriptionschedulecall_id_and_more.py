# Generated by Django 4.1 on 2024-03-21 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0010_alter_subscriptionschedulecall_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionschedulecall',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subscriptionscheduletext',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
