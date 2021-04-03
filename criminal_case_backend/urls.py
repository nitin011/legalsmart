"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from .routers import router
from django.conf import settings
from django.conf.urls.static import static
import djoser.urls.authtoken
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

# from two_factor.urls import urlpatterns as tf_urls

# Additionally, we include login URLs for the browsable API.

# from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token, verify_jwt_token
admin.autodiscover()

# Header and Index of the site
admin.site.site_header = 'Legal Smart App'
admin.site.index_title = 'Legal Smart App'
admin.site.site_title = 'Legal Smart App'

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
	path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    # path('auth/', include('django.contrib.auth.urls')),
	path('api/v1/', include('criminal_case_backend.law.urls')),
    path('api/v1/', include('criminal_case_backend.users.urls')),
    path('api/v1/', include('criminal_case_backend.questionnaire.urls')),
    # path('', include('criminal_case_backend.users.urls')),
    # path('', include('drfpasswordless.urls')),

    # path('users/', include('django.contrib.auth.urls')),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here
    # path('auth/', include('rest_auth.urls')),
    # path('two_factor/', include(tf_urls)),
    # path('get-code-token/', obtain_code_token),
    # path('get-auth-token/', obtain_auth_token),
    # path('auth/', include(djoser.urls.authtoken)),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
    # path('auth/logout/', Logout.as_view()),
    # path("auth/", include("djoser.urls.base")),

    # path('', include('criminal_case_backend.users.urls')),
	# url(r'^answers/',include('answer.urls')),
    # path(r'^rest-auth/', include('rest_auth.urls')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),

    # JWTAUTH
    # path('api-token-auth/', obtain_jwt_token),
    # path('api-token-refresh/', refresh_jwt_token),
    # path('api-token-verify/', verify_jwt_token),

    # path('auth/', include(drf_jwt_2fa.urls, namespace='auth')),
    # path('get-code-token/', obtain_code_token),
    # path('get-auth-token/', obtain_auth_token),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)