from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from . import api
from criminal_case_backend.law.api import *
        
urlpatterns = [
    url(r'^laws/$', LawViewSet1.as_view()),
    url(r'^sub_law/$', SubLawViewSet.as_view()),
    url(r'^sub_law_category/$', SubInnerLawViewSet.as_view()),
    url(r'^final_result/$', FinalResultViewSet.as_view()),
]
