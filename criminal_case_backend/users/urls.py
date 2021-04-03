# from django.conf.urls import include, url
# from rest_framework.routers import DefaultRouter

# from tutorial.users import views

# # Create a router and register our viewsets with it.
# # router = DefaultRouter()
# # # router.register(r'snippets', views.SnippetViewSet)
# # router.register(r'users', views.UserViewSet)

# # # The API URLs are now determined automatically by the router.
# # Additionally, we include the login URLs for the browsable API.
# urlpatterns = [
#     url(r'^', include(router.urls))
# ]

from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
# from . import views
from . import views

from rest_framework.routers import DefaultRouter

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from criminal_case_backend.users.api import *
from . import views
from . import api

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
        
urlpatterns = [
    # url(r'email/',views.email, name = "email"),
    url(r'^user/$', UserViewSet.as_view()),
    url(r'^profile_image/$', profileViewSet.as_view()),
    url(r'^conversion_rate/$', currencyViewSet.as_view()),
    # url(r'^wipay/$', currencyViewSet.as_view()),
    url(r'^wi_pay/$', views.wipay_payment, name='wi_pay'),
    url(r'^return_url/$', views.return_url, name='return_url'),
    # url(r'^success_return_url/$', views.success_return_url, name='success_return_url'),
    url(r'^failed_return_url/$', views.failed_return_url, name='failed_return_url'),
    # url(r'',views.home, name = "home"),
    # url(r'^api/login/$', views.PuppyList.as_view()),
    # url(r'^api/v1/auth/', include(djoser.urls.authtoken)),
    # url(r'^logout/', Logout.as_view()),
    # url(r'^', include(router.urls))
    # url(r'^users/register', 'criminal_case_backend.users.views.create_auth'),
]


# from django.urls import path
# from . import views


# urlpatterns = [path('signup/', views.SignUp.as_view(), name='signup'), ]