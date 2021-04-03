from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, DetailView # Import TemplateView
from django.contrib.auth.decorators import login_required
# from account import views
from django.db.models import Q
import json
from django.http import JsonResponse
from django.db import connection
# from hashids import Hashids
# from hashid_field import HashidField
# from .models import PrivacyType, PrivacyOn, UserPrivacy,BlockedUser,UserSpecificContacts
# from .models import NotificationEventTypes, NotificationType, Notification
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model, logout
from . import serializers
from rest_framework.decorators import action
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from .models import WiPayPayment
# from . import Checksum

# import sentry_sdk
import requests


"""
Method:             settingStat
Developer:          Bhushan
Created Date:       06-03-2018
Purpose:            Setting data
Params:             []
Return:             []
"""
def return_url(request):
    print(request.GET['name'])
    print(request.GET['email'])
    print(request.GET['order_id'])
    print(request.GET['transaction_id'])
    print(request.GET['reasonCode'])
    print(request.GET['reasonDescription'])
    print(request.GET['responseCode'])
    print(request.GET['date'])
    print(request.GET['status'])
    payment = WiPayPayment()
    payment.name = request.GET['name']
    payment.email = request.GET['email']
    payment.order_id = request.GET['order_id']
    payment.transaction_id = request.GET['transaction_id']
    payment.reasonCode = request.GET['reasonCode']
    payment.reasonDescription = request.GET['reasonDescription']
    payment.responseCode = request.GET['responseCode']
    payment.date = request.GET['date']
    payment.total = request.GET['total']
    status = 0
    if request.GET['status'] == "success":
        status = 1
    print(status)    
    payment.save()
    return HttpResponse("<html> Payment Success </html>")
""" end """


"""
Method:             settingStat
Developer:          Bhushan
Created Date:       06-03-2018
Purpose:            Setting data
Params:             []
Return:             []
"""
def failed_return_url(request):
    return HttpResponse("<html> Payment failed </html>")
""" end """


"""
Method:             settingStat
Developer:          Bhushan
Created Date:       06-03-2018
Purpose:            Setting data
Params:             []
Return:             []
"""
def wipay_payment(request):
    return render(request, 'payment.html', {"dashboard": "active"})
    # return HttpResponse("ok")
    # https://sandbox.wipayfinancial.com/v1/gateway
    # MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    # account_number = "3926517936"
    # api_key = "m24p5ro606qr9"

    # MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    # get_lang = "/" + get_language() if get_language() else ''
    # CALLBACK_URL = settings.HOST_URL + get_lang + settings.PAYTM_CALLBACK_URL
	# try:
	# 	send_mail('test', 'hello', 'python.anoop@gmail.com', ['anuop@yopmail.com'])
	# except Exception as e:
	# 	print ("email not send : ", e)
	# from_email = "anup@yopmail.com"
	# emailBody = "Hello"
	# msg = EmailMultiAlternatives("here", emailBody , from_email, ["testi@yopmail.com"])
	# msg.attach_alternative("hello", "text/html",)
	# try:
	# 	# msg.send()
	# 	 send_mail(
	# 			    'Subject here',
	# 			    'Here is the message.',
	# 			    'from@example.com',
	# 			    ['test@yopmail.com'],
	# 			    fail_silently=False,
	# 			)
	# except Exception as e:
	# 	print('There was an error sending an email: ', e)
	# send_mail(
	#     'Subject here',
	#     'Here is the message.',
	#     'from@example.com',
	#     ['test@yopmail.com'],
	#     fail_silently=False,
	# )
	# return HttpResponse("ok")
    # return HttpResponse("<html>Payment failed</html>")
    return HttpResponse("<html><form action='https://sandbox.wipayfinancial.com/v1/gateway' method='post'> <input name='total' type='hidden' value='100'> <input name='total' type='hidden' value='100'></html>")




from rest_framework import permissions, renderers, viewsets
from criminal_case_backend.users.models import User
from .serializers import UserSerializer

class UserViewSet1(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    # print("hello")
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    # print("hello")
    queryset = User.objects.all()
    serializer_class = UserSerializer


from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, logout

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = {serializers.EmptySerializer}
    # serializer_classes = {
    #     'login': serializers.UserLoginSerializer,
    #     'register': serializers.UserRegisterSerializer,
    #     'password_change': serializers.PasswordChangeSerializer,
    # }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        print("I am here only")
        return Response("Ok")

    # @action(methods=['POST', ], detail=False)
    # def register(self, request):
    #     ...

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)


    # @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    # def password_change(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     request.user.set_password(serializer.validated_data['new_password'])
    #     request.user.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def get_serializer_class(self):
     

def home(request):
    return render(request, 'index.html', {})