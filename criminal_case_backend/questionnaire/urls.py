from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from . import api
from criminal_case_backend.questionnaire.api import *
        
urlpatterns = [
    url(r'^questionnaire/$', QuestionnaireViewSet.as_view()), 
    url(r'^need_attorney/$', NeedAttorneyViewSet.as_view()),
    url(r'^not_guilty/$', NotGuiltyViewSet.as_view()),
    url(r'^high_court/$', HighCourtViewSet.as_view()),
    url(r'^trial_choice/$', Trial_ChoiceViewSet.as_view()),
    url(r'^judge_alone_trial/$', Judge_Alone_TrialViewSet.as_view()),
    url(r'^magistrate_court/$', Magistrate_CourtViewSet.as_view()),
    url(r'^to_jurrors/$', To_JurrorsViewSet.as_view()),
    url(r'^trial_by_jury/$', Trial_By_JuryViewSet.as_view()),
    url(r'^sentence/$', SentenceViewSet.as_view()),
    url(r'^tip_information/$', Tip_InformationViewSet.as_view()),
    url(r'^fcm/$', FCMViewSet.as_view()),
    url(r'^need_lawyer/$', NeedLawyerSet.as_view()),
    url(r'^need_lawyer_for/$', NeedLawyerForViewSet.as_view()),
    url(r'^need_bail/$', NeedBailSet.as_view()),
    url(r'^highcourt_questions/$', HighcourtQuestionsViewSet.as_view()),
    url(r'^get_response/$', GetResponseViewSet.as_view()),
    url(r'^response_status/$', ResponseAcceptRejectViewSet.as_view()),
    url(r'^submit_judge_jury/$', ResponseAcceptRejectJudgeViewSet.as_view()),
    url(r'^ticket_pay/$', TicketPayViewSet.as_view()),
    url(r'^ticket_pay_files/$', TicketPayFilesViewSet.as_view()),
    url(r'^attorney_response/$', AttorneyResponseViewSet.as_view()),
    url(r'^challenge_ticket/$', ChallengeTicketViewSet.as_view()),
    url(r'^challenge_ticket_accept/$', ChallengeTicketAcceptViewSet.as_view()),
    url(r'^wipay_status/$', WipayStatusViewSet.as_view()),
    # url(r'^questionnaire_response/$', QuestionnaireResponseViewSet.as_view()),
]
