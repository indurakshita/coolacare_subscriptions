from rest_framework import serializers
from subscription.models.subscription_model import Subscription
from datetime import date ,timedelta
import re

class AlphaCharField(serializers.RegexField):
    def __init__(self, *args, **kwargs):
        kwargs['regex'] = r'^[a-zA-Z]+$'
        kwargs['error_messages'] = {'invalid': 'Please enter only alphabetic characters.'}
        super().__init__(*args, **kwargs)

class NumericField(serializers.RegexField):
    def __init__(self, *args, **kwargs):
        kwargs['regex'] = r'^\d+$'
        kwargs['error_messages'] = {'invalid': 'Please enter only numeric characters.'}
        super().__init__(*args, **kwargs)

class PhoneNumberField(serializers.RegexField):
    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        allow_blank = kwargs.pop('allow_blank', True)
        kwargs['regex'] = r'^\+1\(\d{3}\) \d{3}-\d{4}$'
        kwargs['error_messages'] = {'invalid': 'Please enter a valid US phone number in the format +1(XXX) XXX-XXXX.'}
        super().__init__(*args, **kwargs)
        self.required = required
        self.allow_blank = allow_blank

    # def to_representation(self, value):
    #     digits = ''.join(filter(str.isdigit, value))
    #     # Format the phone number as 3847564389
    #     return digits[-10:]

    # def to_internal_value(self, data):
    #     # Validate the phone number format
    #     if not re.match(r'^\+1\(\d{3}\) \d{3}-\d{4}$', data):
    #         self.fail('invalid')
    #     # data = ''.join(filter(str.isdigit, data))
    #     return data

    def validate_empty_values(self, data):
        if data == '':
            self.fail('invalid')
        return super().validate_empty_values(data)

class SubscriptionSerializer(serializers.ModelSerializer):
    PACKAGE_CHOICES = [
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum'),
    ]

    MODE_OF_CALL_CHOICES = [
        ('SMS', 'SMS'),
        ('VOICE', 'VOICE'),
    ]

    TYPE_OF_CALL_CHOICES = [
        ('COURTESY_CALLS', 'COURTESY_CALLS'),
        ('WELLNESS_CALLS', 'WELLNESS_CALLS'),
        ('PHONE_A_FRIEND', 'PHONE_A_FRIEND'),
        ('MEDICATION_REMINDERS_CALL', 'MEDICATION_REMINDERS_CALL'),
        ('MEAL_REMINDER_CALL', 'MEAL_REMINDER_CALL'),
        ('COURTESY_TEXT', 'COURTESY_TEXT'),
        ('WELLNESS_TEXT', 'WELLNESS_TEXT'),
        ('TEXT_A_FRIEND', 'TEXT_A_FRIEND'),
        ('MEDICATION_REMINDERS_TEXT', 'MEDICATION_REMINDERS_TEXT'),
        ('MEAL_REMINDER_TEXT', 'MEAL_REMINDER_TEXT'),
    ]
    
    PLAN_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]
    STATUS_CHOICES = [
        ('ON HOLD', 'ON HOLD'),
        ('CREATED', 'CREATED'),
        ('ACTIVE', 'ACTIVE'),
        ('EXPIRED', 'EXPIRED'),
        ('CANCELED', 'CANCELED'),
    ]
    id = serializers.IntegerField(required=False)
    first_name = AlphaCharField(max_length=255)
    last_name = AlphaCharField(max_length=255)
    email = serializers.EmailField()
    phone =  PhoneNumberField(required=True)
    package = serializers.ChoiceField(choices=PACKAGE_CHOICES)
    plan = serializers.ChoiceField(choices=PLAN_CHOICES)
    start_date = serializers.DateField(required=False, default=(date.today() + timedelta(days=2)))
    end_date = serializers.DateField(required=False)
    type_of_call = serializers.ChoiceField(choices=TYPE_OF_CALL_CHOICES)
    mode_of_call = serializers.ChoiceField(choices=MODE_OF_CALL_CHOICES)
    message = serializers.CharField(max_length=255)
    communication_email = serializers.EmailField()
    alternate_contact = PhoneNumberField(required=False,allow_blank=True)
    status = serializers.ChoiceField(choices=STATUS_CHOICES,default='ON HOLD')
    acknowledgement = serializers.BooleanField(default=False)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateField(required=False, default=date.today)

    class Meta:
        model = Subscription
        fields = [
            "id", "first_name", "last_name", "email", "phone", "package", "start_date", "end_date", "type_of_call","plan",
            "mode_of_call", "communication_email", "alternate_contact", "status", "acknowledgement", "message",
            "created_by", "created_at"
        ]
    

class CancelSubscriptionSerializer(serializers.Serializer):
    subscription_id = serializers.CharField()