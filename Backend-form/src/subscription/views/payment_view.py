import stripe
from rest_framework.response import Response
from rest_framework.views import APIView
from subscription.serializers.payment_serializer import RefundSerializer
from authapp.validate.validation import validate_response
from rest_framework import status
from django.conf import settings
from authapp.exception import CustomException
from authapp.authentication import JWTAuthenticationBackend
from subscription.models.payment_model import Payment
from subscription.models.subscription_model import Subscription
from subscription.models.slote_model import Slots
from django.contrib.auth import get_user_model
from subscription.tasks import book_slot
from django_q.tasks import async_task
from authapp.utils.email_send import Email_Sender
from authapp.permissions.group_permission import HasGroupPermission
from icecream import ic
User = get_user_model()

class CreatePaymentIntentView(APIView):
    model_name = 'Payment'.lower()
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthenticationBackend]
    def post(self, request):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription_data = Subscription.objects.filter(created_by=request.user.id).last()
            user = User.objects.get(id=request.user.id)

            if subscription_data is None:
                raise CustomException(detail="Subscription data not found", status_code=status.HTTP_400_BAD_REQUEST)

            if subscription_data and subscription_data.trial==False:
                amount_mapping = {
                    ('SILVER', 'monthly'): 1000,
                    ('SILVER', 'yearly'): 10000,
                    ('GOLD', 'monthly'): 2000,
                    ('GOLD', 'yearly'): 20000,
                    ('PLATINUM', 'monthly'): 3000,
                    ('PLATINUM', 'yearly'): 30000,
                }
                
                amount = amount_mapping.get((subscription_data.package, subscription_data.plan.lower()))
                
            elif subscription_data and subscription_data.trial==True:
                amount = 0
                
            else:
                amount = None
            
            if all([user.first_name, user.last_name]):
                session = stripe.checkout.Session.create(
                invoice_creation={"enabled": True},
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"{subscription_data.mode_of_call} SUBSCRIPTION {subscription_data.plan}",
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://subscription.coolocare.com/success',
                cancel_url='https://subscription.coolocare.com/cancel',
                customer_email=subscription_data.email,
                metadata={
                    'username': user.first_name +" "+user.last_name,
                    'subscription_id': subscription_data.id,
                }
                )
                return Response({"chcekout_url": session.url, 
                                 "session_id": session.id
                                 }, status=status.HTTP_201_CREATED)
            else:
                raise CustomException(detail="Please update your profile Details", status_code=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            raise CustomException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)




class HandlePaymentConfirmationView(APIView):
    model_name = 'Payment'.lower()
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthenticationBackend]

    def post(self, request):
        session_id = request.query_params.get('session_id')
        subscription = Subscription.objects.filter(created_by=request.user.id).last()
        try:
            response = self.handle_payment_subscription(session_id,subscription,request)    
            return response            
        except stripe.error.StripeError as e:
            raise CustomException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise CustomException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
            
        
    def handle_payment_subscription(self,session_id,subscription,request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        slots = Slots.objects.filter(subscription=subscription).first()
        if session.payment_status == 'paid' and not slots.booked:
            slots.booked = True
            slots.save()
            Payment.objects.create(payment_indent_id=session.payment_intent,
                                subscription_id=subscription,
                                payment_confirmation=session.payment_status)
            subscription.status = "CREATED"
            subscription.save()
            Email_Sender(
                subject="Subscription Confirmation",
                template_name="Subscription_confirm.html",
                context={
                "plan": subscription.package,
                "name": subscription.first_name+" "+subscription.last_name,
                "email":subscription.email,
                "cycle" :subscription.plan if not slots.trial else f"TRIAL 30 days + {subscription.plan}",
                "start_date": subscription.start_date,
                "end_date": subscription.end_date,
                },

                recipient_list=subscription.email
            )
            plan = 365 if subscription.plan == "YEARLY" else 30
            plan = plan + 30 if slots.trial==True else plan
            kwargs = {
                'request': subscription,
                'slotes': slots,
                "plan": plan
            }
            async_task(func=book_slot, **kwargs)
            return validate_response("PaymentSuccess")
        
        elif session.payment_status == 'paid' and slots.booked:
            return validate_response("SlotesAlredyBooked")
        
        else:
            Payment.objects.create(payment_indent_id=session.url,
                                subscription_id=subscription,
                                payment_confirmation=session.payment_status)
            subscription.status = "CANCELLED"
            subscription.save()
            return validate_response("PaymentCancel")
       
    

class RefundView(APIView):
    model_name = 'Payment'.lower()
    permission_classes = [HasGroupPermission]
    authentication_classes = [JWTAuthenticationBackend]
    
    def post(self, request):
        serializer = RefundSerializer(data=request.data)
        if serializer.is_valid(): 
            intent_id = serializer.validated_data.get('intent_id')
            gateway_data = {
                "secretKey": settings.STRIPE_SECRET_KEY
            }
            try:
                stripe.api_key = gateway_data["secretKey"]
                refund_status = stripe.Refund.create(
                    payment_intent=intent_id
                )
                return Response({"status": "Success", "code": 200})
            except stripe.error.InvalidRequestError as e:
                raise CustomException(detail = str(e),status_code=status.HTTP_400_BAD_REQUEST)
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)