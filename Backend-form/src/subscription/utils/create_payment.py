from subscription.models.payment_model import Payment
from django.conf import settings
import stripe


def create_payment_record(self, session, subscription):
        Payment.objects.create(
            payment_indent_id=session.payment_intent,
            subscription_id=subscription,
            payment_confirmation=session.payment_status
        )

def retrieve_stripe_session(self, session_id):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return stripe.checkout.Session.retrieve(session_id)