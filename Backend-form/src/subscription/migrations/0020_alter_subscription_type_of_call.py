# Generated by Django 4.1 on 2024-04-08 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0019_alter_schedulestatus_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='type_of_call',
            field=models.CharField(choices=[('COURTESY_CALLS', 'COURTESY_CALLS'), ('WELLNESS_CALLS', 'WELLNESS_CALLS'), ('PHONE_A_FRIEND', 'PHONE_A_FRIEND'), ('MEDICATION_REMINDERS_CALL', 'MEDICATION_REMINDERS_CALL'), ('MEAL_REMINDER_CALL', 'MEAL_REMINDER_CALL'), ('COURTESY_TEXT', 'COURTESY_TEXT'), ('WELLNESS_TEXT', 'WELLNESS_TEXT'), ('TEXT_A_FRIEND', 'TEXT_A_FRIEND'), ('MEDICATION_REMINDERS_TEXT', 'MEDICATION_REMINDERS_TEXT'), ('MEAL_REMINDER_TEXT', 'MEAL_REMINDER_TEXT')], max_length=255),
        ),
    ]
