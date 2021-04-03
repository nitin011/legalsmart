from django.db import models
from django.core import serializers
from criminal_case_backend.users.models import User
from criminal_case_backend.law.models import LawInnerCategory
import datetime
import uuid

Questionaire_Type = (
        ('accused', 'accused'),
        ('victim', 'victim'),
        ('offence', 'offence')
    )

Option_Type = (
        ('1', 'Radio'),
        ('2', 'Dropdown'),
        ('3', 'Spinner'),
        ('4', 'Text')
    )
class QuestionnaireType(models.Model):
    q_type = models.CharField(max_length=250, blank=False, unique=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)

    class Meta:
         db_table = "questionaire_type"
         verbose_name_plural = "Questionnaire Type"
    
    def __str__(self):
        return self.q_type

class Questionnaire(models.Model):
    name = models.CharField(max_length=350,blank=False,unique=False)
    option = models.CharField(max_length=350,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    updated_at =models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        # unique_together = ('name', 'law_inner_category')

        # constraints = [models.UniqueConstraint(fields=['name', 'law_inner_category'], name='UniqueConstraint')]

        db_table = "questionnaires"
        verbose_name_plural = "Questionnaire"
    
    def __str__(self):
        return self.name

import calendar
AGE_CHOICE = [(str(i), str(i)) for i in range(1,101)]
MONTH_CHOICE = [(str(i), calendar.month_name[i]) for i in range(1,13)]

class Age(models.Model):
    age = models.CharField(choices=MONTH_CHOICE, max_length=250, blank=False, unique=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)

    class Meta:
         db_table = "age_group"
         verbose_name_plural = "Age Group"
    
    def __str__(self):
        return self.age

API_CHOICE = (
        ('need_atterney', 'need_atterney'),
        ('not_guilty', 'not_guilty'),
        ('judge_alone_trial', 'judge_alone_trial'),
        ('magistrate_court', 'magistrate_court'),
        ('to_jurrors', 'to_jurrors'),
        ('trial_by_jury', 'trial_by_jury'),
        ('sentence', 'sentence'),
        ('tip_information', 'tip_information'),
    )
class StaticContentApi(models.Model):
    api_name = models.CharField(choices=API_CHOICE, max_length=80, blank=False, unique=False)
    option1 = models.TextField(blank=True,null=True)
    option2 = models.TextField(blank=True,null=True)
    note = models.TextField(blank=True,null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)

    class Meta:
         db_table = "static_content_api"
         verbose_name_plural = "Content for API"
    
    def __str__(self):
        return self.api_name

class QuesAnswer(models.Model):
    # ques = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    answer = models.TextField(max_length=5000,blank=True, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    device_id = models.CharField(max_length=120, blank=False ,null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)

    class Meta:
         db_table = "questionnaire_answers"
         verbose_name_plural = "Questionnaire Answer"
    
    def __str__(self):
        return self.answer


USER_CHOICE = (
        ('need_a_atterney', 'need_a_atterney'),
        ('need_a_lawyer', 'need_a_lawyer'),
        ('need_bail', 'need_bail'),
    )

class UserResponse(models.Model):
    response_for = models.CharField(choices=USER_CHOICE, max_length=80, blank=False, unique=False, null=True)
    needed_for_law = models.CharField(max_length=80, blank=False, unique=False, null=False)
    needed_for_options = models.CharField(max_length=800, blank=False, unique=False, null=False)
    name = models.CharField(max_length=120, blank=False ,null=True)
    contact_info = models.CharField(max_length=120, blank=False ,null=True)
    date = models.CharField(max_length=120, blank=False ,null=True)
    device_id = models.CharField(max_length=120, blank=False ,null=True)
    option = models.CharField(max_length=120, blank=False ,null=True)
    offence = models.CharField(max_length=120, blank=False ,null=True)
    appearance = models.CharField(max_length=120, blank=False ,null=True)

    comment = models.CharField(max_length=500, blank=False ,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='lawyer')
    
    status = models.CharField(max_length=120,default='',blank=False ,null=True)
    is_authorise_check = models.CharField(max_length=120,default='',blank=False ,null=True)
    is_age_check = models.CharField(max_length=120,default='',blank=False ,null=True)

    class Meta:
         db_table = "User_requests"
         verbose_name_plural = "User Requests for"
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-NA-"

TICLKET_STATUS = (
        ('1', 'Success'),
        ('2', 'Failed'),
    )
CURRENCY = (
        ('1', 'USD'),
    )
class Ticket(models.Model):
    ticket_status = models.CharField(choices=TICLKET_STATUS, default="", max_length=80, blank=False, unique=False, null=True)
    name = models.CharField(max_length=200, blank=True ,null=True)
    # last_name = models.CharField(max_length=200, blank=False ,null=True)
    email = models.CharField(max_length=200, blank=True ,null=True)
    phone_number = models.CharField(max_length=20, blank=True ,null=True)
    device_id = models.CharField(max_length=120, blank=True ,null=True)
    ticket_order_id = models.CharField(max_length=120, blank=True ,null=True)
    amount = models.CharField(max_length=50, blank=True ,null=True)
    currency = models.CharField(choices=CURRENCY, default="USD", max_length=120, blank=True ,null=True)

    idUrl = models.CharField(max_length=250, blank=True ,null=True)
    ticket_url = models.CharField(max_length=250, blank=True ,null=True)
    challenge_status = models.CharField(max_length=50, blank=True ,null=True)
    permit = models.CharField(max_length=200, blank=True ,null=True)
    total_amount = models.CharField(max_length=50, blank=True ,null=True)
    total_amount_USD = models.CharField(max_length=50, blank=True ,null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ticket_user')

    class Meta:
         db_table = "tickets"
         verbose_name_plural = "Tickets"
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-NA-"

class ChallangeTicket(models.Model):
    rep_status = models.BooleanField(default=False)
    accepted_by_name = models.CharField(max_length=120,default='',blank=False ,null=True)
    accepted_by_contact = models.CharField(max_length=120,default='',blank=False ,null=True)
    rep_deadline = models.CharField(max_length=200, blank=False ,null=True)
    notice_ref_number = models.CharField(default="", max_length=300, blank=False, unique=False, null=True)
    vehicle_reg_number = models.CharField(default="", max_length=300, blank=False, unique=False, null=True)
    driver_permit_number = models.CharField(default="", max_length=300, blank=False, unique=False, null=True)
    notice_issue = models.CharField(default="", max_length=300, blank=False, unique=False, null=True)
    reason = models.CharField(max_length=2000, blank=False ,null=True)
    challange_ticket = models.BooleanField(default=True)
    name = models.TextField(max_length=200,blank=True,null=True)
    deadline_comingup = models.TextField(max_length=200,blank=True,null=True)
    file_url = models.TextField(max_length=300,blank=True,null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='challange_ticket_user')
    accept_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='challange_ticket_user_accept')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)


    class Meta:
         db_table = "challange_tickets"
         verbose_name_plural = "Challange Tickets"
    
    def __str__(self):
        if self.reason:
            return self.reason  
        else:
            return "-NA-"