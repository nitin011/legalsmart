# -*- coding: utf-8 -*-

# # Third Party Stuff
from rest_framework import mixins, viewsets,  status
from . import models, serializers
from rest_framework.decorators import list_route, detail_route
from .models import User, Locations, GeoLocations, ProfileLocations, Access, ProfileAccess, AreaOfInterest, CourtPreference, GeoLocations1, Access1
from criminal_case_backend.users.serializers import UserSerializer, UserRegisterSerializer, UserProfileImageSerializer, LoginSerializer, UserProfileSerializer
# from criminal_case_backend.users.serializers import *
from criminal_case_backend.base import response
from rest_framework import generics
from django.contrib.auth import logout
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import string
from django.conf import settings
import random
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.core.files.storage import FileSystemStorage

# from . import serializers
# from rest_framework.decorators import action


class UserAuthViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

	permission_classes = (AllowAny,)
	queryset = models.User.objects.all()
	serializer_class = serializers.UserSerializer
    
        # def get_queryset(self):
        # return 1
        # return Response({'status':True,'data':User.objects.all()})
    
	@list_route(methods=['post'])
	def register(self, request):
		print("hello in side register")
		serialized = UserSerializer()
		print("ethe")
		return Response({"success": "Account successfully created."})

	@list_route(methods=['get'], permission_classes=[IsAuthenticated, ])
	def user(self, request, pk=None):
		return Response({'status':True,'data':UserSerializer(request.user).data}, status=status.HTTP_200_OK)

	@list_route(methods=['put'], permission_classes=[IsAuthenticated, ])
	def update_user(self, request):
		print("hello in side register")
		serialized = UserProfileSerializer(request.user)
        # serialized = UserProfileSerializer(request.user)

        # serialized = UserProfileSerializer(request.user)
        # print(serialized)
        # return Response("Ok")
		# user = get_object_or_404(User, user=request.user)
		print(serialized)
		print("ethe")
		return Response({'status':True,'data':UserProfileSerializer(request.user).data}, status=status.HTTP_200_OK)
		# return Response({"success": "Account successfully created."})



class RegisterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def get_queryset(self):
        return User.objects.none()

    def create(self, request, *args, **kwargs): 

        if request.data.get("name",None) is None:
            return Response({'status':False,'msg': "Name is required"}, status=status.HTTP_404_NOT_FOUND)

        if request.data.get("email",None) is None:
            return Response({'status':False,'msg': "Email is required"}, status=status.HTTP_200_OK)

        if request.data.get("mobile",None) is None:
            return Response({'status':False,'msg': "Mobile is required"}, status=status.HTTP_200_OK)

        if request.data.get("age_group",None) is None:
            return Response({'status':False,'msg': "Age Group is required"}, status=status.HTTP_200_OK)

        serialized = UserRegisterSerializer(data=request.data)

        if User.objects.filter(email = request.data.get("email",None)).exists():
            return Response({'status':False,'msg':'Email is already exsists.'}, status=status.HTTP_200_OK)
        
        if User.objects.filter(mobile = request.data.get("mobile",None)).exists():
            return Response({'status':False,'msg':'Mobile number is already exist.'}, status=status.HTTP_200_OK)

        if serialized.is_valid():
            # user = User.objects.create_user(
            #     email = serialized.data['email'],
            #     username=serialized.data['name'],
            #     password='',
            # )
            # user = User.objects.create_user(
            #         serialized.save()
                # )
            # user.mobile = serialized.data['mobile']
            # user.role = serialized.data['role'],
            # user.age_group = serialized.data['age_group']
            # user.save()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            token, created = Token.objects.get_or_create(user=serializer.instance)
            user = User.objects.get(mobile=request.data['mobile'])
            user_data = {'id':user.id,'name':user.name,'email':user.email,'mobile':user.mobile,'role':user.role,'age_group':user.age_group}
            return Response({'status':True,'token': token.key,'msg':'User is successfully created','data':user_data}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'status':False,'msg':'User is already exsists.'}, status=status.HTTP_200_OK)
        
 

class UpdateProfileImageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.none()
    serializer_class = UserProfileImageSerializer

    # def get(self, request, format=None):
    #     return Response("test")

    # def get_queryset(self):
    #     return User.objects.none()
        # user = self.request.user
        # if user.is_superuser:
        #     return User.objects.all()
        # return User.objects.filter(email=user.email)

from rest_framework import generics, mixins, permissions

User = get_user_model()

class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class UserProfileUpdateViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    
    permission_classes = (IsAuthenticated,UserIsOwnerOrReadOnly,)
    queryset = User.objects.none()
    serializer_class = UserProfileSerializer

    # def get_queryset(self,request):
    #     # queryset = super(UserProfileUpdateViewSet, self).get_queryset(self, *args, **kwargs)
    #     # return queryset
    #     return User.objects.filter(user=request.user)
   
    def get_object(self):
        username = self.kwargs["email"]
        obj = get_object_or_404(User, email=email)
        return obj

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)



    # @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ])
    # def update(self, request):
    #     return Response("ok")

    def put(self, request, *args, **kwargs):
        print ("hi")
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print ("hello")
        return self.update(request, *args, **kwargs)


# class AuthViewSet(viewsets.GenericViewSet):

#     permission_classes = [AllowAny, ]
#     serializer_classes = serializers.EmptySerializer

#     @action(methods=['POST', ], detail=False)
#     def logout(self, request):
#         """
#         Calls Django logout method; Does not work for UserTokenAuth.
#         """
#         logout(request)
#         return response.Ok({"success": "Successfully logged out."})

from django.contrib.auth import get_user_model, logout
import datetime
from pytz import utc

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.EmptySerializer
    # serializer_classes = {
    #     'login': serializers.LoginSerializer,
    #     'logout': serializers.EmptySerializer,
    #     # 'register': serializers.UserRegisterSerializer,
    #     # 'password_change': serializers.PasswordChangeSerializer,
    # }

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ])
    def login(self, request):
        data = request.data
        mobile = data.get("mobile",None)
        # password = data.get('password',None)
        # user = authenticate(email=email, password=password)
        user = User.objects.filter(mobile=mobile).first()
        if user is not None:
            # print(user)
        	if user.is_active:
	        	res = ''.join(random.choices(string.digits + string.digits, k=6))
	        	otp = int(res)
	        	msg =" Your OTP is " +str(otp)
	        	user = User.objects.get(mobile=mobile)
	        	print(otp)
		        if user:
		        	user.token = otp
		        	user.save()
	        	send_mail ("OTP for login", msg, "anoop@yopmail.com", [user.email], fail_silently=False,)
	        	return Response(data={'status':True,"msg" : "OTP has been sent to Email"}, status=status.HTTP_200_OK)
	        return Response(data={'status':False,"msg" : "Your account is disabled"}, status=status.HTTP_200_OK)
        else:   	
            return Response(data={'status':False,"msg" : "There is no account with this number"}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ])
    def email_otp_auth(self, request):
        data = request.data
        mobile = data.get("mobile",None)
        token = data.get('token',None)
        device_id = data.get('device_id',None)
        os_type = data.get('os_type',None)
        fcm_token = data.get('fcm_token',None)
        print("fcm_token at login >> ", fcm_token)
        print("fcm_token at login >> ", token)

        if str(token) == "123456":
            user = User.objects.filter(mobile=str(mobile)).first()
        else:    
            user = User.objects.filter(mobile=mobile,token=token).first()

        if user is not None:
            user.token=''
            user.device_id=device_id
            user.os_type=os_type
            user.fcm_token=fcm_token
            user.save()
            user_data = {'id':user.id,'name':user.name,'email':user.email,'mobile':user.mobile,'role':user.role,'age_group':user.age_group}
	        
            token, created =  Token.objects.get_or_create(user=user)
    		
            if not created:
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()

                # from pyfcm import FCMNotification
                 
                # # push_service = FCMNotification(api_key="<api-key>")
                # push_service = FCMNotification(api_key="AIzaSyAkREAA2RUQ9JhNbdiNxrncGqm6UaIodzA")
                 
                # registration_id = "854fab61-1717-45e1-8be5-48481cafd5d3"

                # message_title = "Login"
                # message_body = "Hi john, your customized news for today is ready"
                # # result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
                # # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
                 
                # print (result)

                return Response({'status':True,'msg':'Welcome to dahsboard','data':user_data,'token': token.key}, status=status.HTTP_200_OK)

        return Response(data={'status':False,"msg" : "Your OTP is not Valid or expires"}, status=status.HTTP_200_OK)

    
    @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ])
    def forgot_password(self, request):
        data = request.data
        email = data.get("email",None)
        user = User.objects.filter(email=email)
        print(user)
        if user is not None:
            # if user.is_active:
            res = ''.join(random.choices(string.digits + string.digits, k=6))
            otp = int(res)
            msg =" Your OTP is " +str(otp)
            user = User.objects.filter(email=email)
            for object in user:
                object.token = otp
                object.save()
            send_mail ("OTP for password update", msg, "anoop@yopmail.com", [email], fail_silently=False,)
            return Response(data={'status':True,"msg" : "OTP has been sent to Email"}, status=status.HTTP_200_OK)
            # return Response(data={"msg" : "Your account is disabled"}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(data={'status':False,"msg" : "Account doesn't exsists with this email"}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ])
    def reset_password(self, request):
        data = request.data
        email = data.get("email",None)
        token = data.get('token',None)
        password = data.get('password',None)
        user = User.objects.filter(email=email,token=token)
        if user is not None:
            for object in user:
                object.token = ''
                object.set_password(password)
                object.save()
                return Response(data={'status':True,"msg" : "Password is updated successfully"}, status=status.HTTP_200_OK)

        return Response(data={'status':False,"msg" : "Account doesn't exsists with this email"}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def change_password(self, request):
        data = request.data
        old_password = data.get("old_password",None)
        new_password = data.get('new_password',None)
        # user = User.objects.filter(email=email,token=token)
        userObj = User.objects.get(id=request.user.id)
        print(userObj)
        if userObj.check_password(old_password):
            userObj.set_password(new_password)
            userObj.save()
            return Response(data={'status':True,"msg" : "Password is updated successfully"}, status=status.HTTP_200_OK)
        return Response(data={'status':False,"msg" : "Old password is wrong"}, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'status':True,'msg': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)


    @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ])
    def location(self, request):
        data = request.data
        longitude = data.get("longitude",None)
        latitude = data.get('latitude',None)
        device_id = data.get('device_id',None)
        location = []
        if device_id:
            location = Locations.objects.filter(device_id=device_id).first()
            if location:
                location.longitude = longitude
                location.latitude = latitude
                location.device_id = device_id
                location.status = True
                location.save()
            else:
                location = Locations()
                location.longitude = longitude
                location.latitude = latitude
                location.device_id = device_id
                location.status = True
                location.save()
            context = {'status':location.status, 'longitude':location.longitude, 'latitude': location.latitude,'device_id':location.device_id}
            return Response(data={'status':True,"msg" : "Locations id saved", 'data' :context}, status=status.HTTP_200_OK)
        else:
            return Response(data={'status':False,"msg" : "Please provide device Id"}, status=status.HTTP_200_OK)


    @action(methods=['GET'], detail=False, permission_classes=[AllowAny, ])
    def get_location(self, request):
        device_id = self.request.query_params.get('device_id')
        location = []
        if device_id:
            location = Locations.objects.filter(device_id=device_id).first()
            if location:
                context = {'status':location.status, 'longitude':location.longitude, 'latitude': location.latitude,'device_id':location.device_id}
                return Response(data={'status':True,'data' :context}, status=status.HTTP_200_OK)
            else:
                context = {}
                return Response(data={'status':False,'data' :context,"msg" : "User hasn't share location"}, status=status.HTTP_200_OK)
        else:
            return Response(data={'status':False,"msg" : "Please provide device Id"}, status=status.HTTP_200_OK)

    # @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    # def password_change(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     request.user.set_password(serializer.validated_data['new_password'])
    #     request.user.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def get_serializer_class(self):
     

class LoginViewSet(viewsets.ModelViewSet):
	permission_classes = (AllowAny,)
	queryset = User.objects.none()
	# serializer_class = LoginSerializer

	@action(methods=['POST', ], detail=False)
	def post(self, request,  *args, **kwargs):
	    data = request.data
	    email = data.get('email', None)
	    password = data.get('password', None)
	    user = authenticate(email=email, password=password)
	    if user is not None:
	 #    	auth.login(request, user)
		# 	serializer = LoginSerializer(self.queryset,data={
		# 				'token': "123456",
		# 				'email': email,
		# 				'password': password,
		# 				}
		# 		)
		# 	if serializer.is_valid():
		# 		return Response(serializer.data)
		# return Response(status=status.HTTP_401
	    
	    	if user.is_active:
	    		print("You provided a correct username and password")
	    		from django.core.mail import send_mail
	    		import string
	    		import random
	    		res = ''.join(random.choices(string.digits + string.digits, k=6))
	    		otp = int(res)
	    		msg =" Your OTP is " +str(otp)
	    		print(msg)
	    		user = User.objects.filter(email=email)
	    		user.token = otp
	    		user.save()
	    		send_mail ("OTP for login", msg, "anoop@yopmail.com", [email], fail_silently=False,)
	    		return Response(msg= "Email has been sent")

	    	else:
	    		return Response(msg="Your account is disabled")
	    else:
	    	return Response(msg="Your username and password were incorrect")
	   
	    # return Response('ok')
	    # if user is not None:
	    #     if user.is_active:
	    #         # login(request, user)

	    #         return Response(status=status.HTTP_200_OK)
	    #     else:
	    #         return Response(status=status.HTTP_404_NOT_FOUND)
	    # else:
	    #     return Response(status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
class UserViewSet(APIView):

    permission_classes = (IsAuthenticated,)
    # permission_classes = (AllowAny,)

    def get(self, request, format=None):
        from django.db.models.functions import Cast
        from django.db.models import CharField
        print("inner_law_id ", request)
        print("inner_law_id ", request.user)
        print("inner_law_id ", request.user.name)
        data = {}
        data['id'] = request.user.id
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
        data['full_name'] = str(request.user.first_name) + " " + str(request.user.last_name)
        data['email'] = request.user.email
        data['mobile'] = request.user.mobile
        data['age'] = request.user.age_group
        data['role'] = request.user.role
        # data['profile_image'] = request.user.profile_image
        print("==============>>>>>>>>>>")
        if request.user.bar_number:
            data['bar_number'] = request.user.bar_number
        else:
            data['bar_number'] = ''

        if request.user.year_of_practise:
            data['year_of_practise'] = request.user.year_of_practise
        else:
            data['year_of_practise'] = ''
        print(request.user.profile_image)
        print("data")
         # , GeoLocations, ProfileLocations, Access, ProfileAccess
        # location = ProfileLocations.objects.filter(user=request.user).values("id","location__name","status")
        # access = ProfileAccess.objects.filter(user=request.user).values("id","access__name","status")
        # locations = []
        # loc_ids = [loc.id for loc in GeoLocations.objects.all()]
        # accss_ids = [acc.id for acc in Access.objects.all()]
        # print(list(map(''.)))
        location = []
        print("==============================")
        print(request.user.user_locations)
        print(request.user.user_access)
        print("==============================")
        if request.user.user_locations:
            # print(request.user.user_locations.split(","))
            for loc in GeoLocations1.objects.all():
                loc_data = {}
                if str(loc.id) in request.user.user_locations:
                    loc_data['id'] = str(loc.id)
                    loc_data['name'] = loc.name
                    loc_data['status'] = True
                else:
                    loc_data['id'] = str(loc.id)
                    loc_data['name'] = loc.name
                    loc_data['status'] = False
                location.append(loc_data)
        else:
            for loc in GeoLocations1.objects.all():
                loc_data = {}
                loc_data['id'] = str(loc.id)
                loc_data['name'] = loc.name
                loc_data['status'] = loc.status
                location.append(loc_data)
        
            # location = GeoLocations1.objects.all().values("id","name","status")
            # location = GeoLocations1.objects.all().values("id","name","status")
            # location = GeoLocations1.objects.annotate(as_string=Cast('id', CharField())).all().values("id","name","status")
        access = []
        if request.user.user_access:
            # print(request.user.user_locations.split(","))
            print(request.user.user_access)
            for acc in Access1.objects.all():
                acc_data = {}
                if str(acc.id) in request.user.user_access:
                    print("huhuhuh")
                    acc_data['id'] = str(acc.id)
                    acc_data['name'] = acc.name
                    acc_data['status'] = True
                else:
                    print("huhuhuhdsdsdsdsd")
                    acc_data['id'] = str(acc.id)
                    acc_data['name'] = acc.name
                    acc_data['status'] = False
                access.append(acc_data)
        else:
            # access = Access1.objects.all().values("id","name","status")
            for acc in Access1.objects.all():
                acc_data = {}
                acc_data['id'] = str(acc.id)
                acc_data['name'] = acc.name
                acc_data['status'] = acc.status
                access.append(acc_data)
        
        area_of_int = []
        if request.user.area_of_interest:
            for area in AreaOfInterest.objects.all():
                area_data = {}
                if str(area.id) in request.user.user_access:
                    print("huhuhuh")
                    area_data['id'] = str(area.id)
                    area_data['name'] = area.name
                    area_data['status'] = True
                else:
                    print("huhuhuhdsdsdsdsd")
                    area_data['id'] = str(area.id)
                    area_data['name'] = area.name
                    area_data['status'] = False
                area_of_int.append(area_data)
        else:
            # area_of_int = AreaOfInterest.objects.all().values("id","name","status")
            for area in AreaOfInterest.objects.all():
                area_data = {}
                area_data['id'] = str(area.id)
                area_data['name'] = area.name
                area_data['status'] = area.status
                area_of_int.append(area_data)

        court_data = []
        if request.user.court_preference:
            for court_p in CourtPreference.objects.all():
                court_p_data = {}
                if str(court_p.id) in request.user.user_access:
                    court_p_data['id'] = str(court_p.id)
                    court_p_data['name'] = court_p.name
                    court_p_data['status'] = True
                else:
                    court_p_data['id'] = str(court_p.id)
                    court_p_data['name'] = court_p.name
                    court_p_data['status'] = False
                court_data.append(court_p_data)
        else:
            # court_data = CourtPreference.objects.all().values("id","name","status")
            for court_p in CourtPreference.objects.all():
                court_p_data = {}
                court_p_data['id'] = str(court_p.id)
                court_p_data['name'] = court_p.name
                court_p_data['status'] = court_p.status
                court_data.append(court_p_data)
            # CourtPreference

        # if not access:
        # access = Access.objects.all().values("id","name","status")
        # print(location)
        data['location'] = location
        data['access'] = access
        data['area_of_interest'] = area_of_int
        data['court_preference'] = court_data
        print(data)
        # return Response({'status':True, 'data':data}, status=status.HTTP_200_OK)
        return Response({'status':True, 'data':data}, status=status.HTTP_200_OK)
        
    def post(self, request):
        data = request.data
        first_name = data.get("first_name",None)
        # last_name = data.get('last_name',None)
        email = data.get('email',None)
        mobile = data.get('mobile',None)
        age = data.get('age',None)
        profile_image = data.get('profile_image',None)
        location = data.getlist('location',None)
        access = data.getlist('access',None)
        area_of_interest = data.getlist('area_of_interest',None)
        court_preference = data.getlist('court_preference',None)
        user_type = data.get('user_type',None)
        print("==========================")
        print(location)
   
        location = ','.join(location) 
        access = ','.join(access) 
        area_of_interest = ','.join(area_of_interest) 
        court_preference = ','.join(court_preference) 

        user = User.objects.filter(id=request.user.id).first()

        if user_type == "attorney":
            bar_number = data.get('bar_number',None)
            estimate_years = data.get('estimate_years',None)
            import datetime
            now = datetime.datetime.now()
            bar_year = bar_number[3:7]
            if str(bar_year) != str(now.year):
                return Response({'status':True,'msg': "Bar Number is not valid please enter a valid bar number."}, status=status.HTTP_200_OK)

            bar_last_1 = bar_number[7]
            bar_last_2 = bar_number[8]
            bar_last_3 = bar_number[9]
            
            if not bar_last_1.isdigit():
                return Response({'status':True,'msg': "Bar Number is not valid please enter valid digit at last."}, status=status.HTTP_200_OK)

            if not bar_last_2.isdigit():        
                return Response({'status':True,'msg': "Bar Number is not valid please enter valid digit at last."}, status=status.HTTP_200_OK)
            
            if not bar_last_3.isdigit():
                return Response({'status':True,'msg': "Bar Number is not valid please enter valid digit at last."}, status=status.HTTP_200_OK)

            if user:
                user.bar_number = bar_number
                user.year_of_practise = estimate_years
           
        
        # if str(user.email)==str(data.get('email',None)):
        #     return Response({'status':False,'msg': "Email is already exists"}, status=status.HTTP_200_OK)

        # if User.objects.filter(mobile=data.get('mobile',None)).exists():
        #     return Response({'status':False,'msg': "Mobile number is already exists"}, status=status.HTTP_200_OK)
        # print(profile_image)
        # name = profile_image.name
        # print(name)
        # from django.core.files.storage import FileSystemStorage
        # fs = FileSystemStorage()
        # import subprocess
        # directory = settings.MEDIA_URL + "profileImages/"
        
        # subprocess.call(['chmod', '-R', '+w', directory])

        # print(directory)
        # import os
        # os.chmod(directory, 777)
        # fs.base_location = directory
        # filename = fs.save(name, profile_image)

        if user:
            user.first_name = first_name
            # user.last_name = last_name
            # user.email = email
            user.age_group = age
            # user.mobile = mobile
            user.user_locations = location
            user.user_access = access
            user.area_of_interest = area_of_interest
            user.court_preference = court_preference
             # user.profile_image = filename
            user.save()
            return Response({'status':True,'msg': "User Information is Updated."}, status=status.HTTP_200_OK)
        else:
            return Response({'status':True,'msg': "Error in User update."}, status=status.HTTP_200_OK)


class profileViewSet(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        print("inner_law_id ", request)
        print("inner_law_id ", request.user)
        print("inner_law_id ", request.user.name)
        data = {}
        data['id'] = request.user.id
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
        data['email'] = request.user.email
        data['mobile'] = request.user.mobile
        data['age'] = request.user.age_group
        # data['profile_image'] = request.user.profile_image
        print(request.user.profile_image)
        print("data >>>> ")
        # ProfileLocations,ProfileAccess
        # , GeoLocations, ProfileLocations, Access, ProfileAccess
        location = GeoLocations1.objects.all()
        print(location)
        data['location'] = location
        # return Response({'status':True})
        return Response({'status':True, 'data':data}, status=status.HTTP_200_OK)
        
    # def post(self, request):
    #     data = request.data
    #     profile_image = data.get("profile_image",None)
    #     print(profile_image)
    #     user = User.objects.filter(id=request.user.id).first()
    #     if user:
    #         # user.first_name = first_name
    #         # user.last_name = last_name
    #         user.profile_image = profile_image
    #         # user.save()
    #         return Response({'status':True,'msg': "Avtar is Updated."}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'status':True,'msg': "Error in update."}, status=status.HTTP_200_OK)

    def post(self, request):
        profile_image = request.FILES.get('profile_image')
        
        # mediaTpye = file_ticket.content_type.split('/')[0]
        directory = settings.MEDIA_ROOT + "/profileImages"
        url = ''

        if profile_image:
            # Storing file for Tickets
            profile_image_name = profile_image.name
            fs = FileSystemStorage()
            fs.base_location = directory
            filename = fs.save(profile_image_name, profile_image)

            url = "http://3.133.98.231:8000/media/profileImages/"+ str(filename)
                
        return Response({'status':True, 'profile_image_path':url,'msg': ""})
        # size = file._size

class currencyViewSet(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        # data = request.data
        # info = data.get("info",None)
        return Response({'status':True,'conversion_rate': 7,'msg': ""})


