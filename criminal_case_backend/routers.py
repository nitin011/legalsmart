# -*- coding: utf-8 -*-
'''This urls.py is for all API related URLs.

URL Naming Pattern (lowercased & underscored)
<app_name>_<model_name> or
<app_name>_<specific_action>

For base name use:
<app_name>
'''

# Third Party Stuff
from rest_framework import routers
# from criminal_case_backend.users.api import UserAuthViewSet, RegisterViewSet, AuthViewSet, UpdateProfileImageViewSet, UserProfileUpdateViewSet
from criminal_case_backend.users.api import *
from criminal_case_backend.law.api import *
# from users import views
from criminal_case_backend.users import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'register', RegisterViewSet, base_name='register')
router.register(r'users', UserAuthViewSet, base_name='users')
router.register(r'update_profile_image', UpdateProfileImageViewSet, base_name='update_profile_image')
router.register(r'update_profile', UserProfileUpdateViewSet, base_name='update_profile')
router.register('', AuthViewSet, basename='auth')
# router.register('locations', AuthViewSet, basename='auth')
# router.register('laws', LawViewSet, basename='law')
# router.register('sub_law', SubLawViewSet, basename='sub_law')

