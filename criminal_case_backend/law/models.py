from django.db import models
from django.core import serializers
from criminal_case_backend.users.models import User
import datetime
import uuid


#block User List
class Law(models.Model):
    laws = models.CharField(max_length=50,blank=False,unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)

    class Meta:
         db_table = "laws"
         verbose_name_plural = "Law"
    
    def __str__(self):
        return self.laws

class LawCategory(models.Model):
    law = models.ForeignKey(Law, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=False,unique=True)
    is_active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)

    class Meta:
         db_table = "law_category"
         verbose_name_plural = "law category"

    def __str__(self):
        return self.name

class LawInnerCategory(models.Model):
    law = models.ForeignKey(LawCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=False,unique=True)
    description_1 = models.TextField(max_length=1000, blank=True,unique=False, verbose_name="Description 1")
    description_2 = models.TextField(max_length=1000, blank=True,unique=False, verbose_name="Description 2")
    summary_offence = models.BooleanField(default=False,verbose_name="Summary Offence")
    indictable_offence = models.BooleanField(default=False,verbose_name="Indictable Offence")
    is_active = models.BooleanField(default=False)
    
    # result pages
    sentence_by_magistrate = models.TextField(max_length=1000, blank=True,unique=False, verbose_name="SENTENCE by Magistrate")
    appeal_court = models.CharField(max_length=250,blank=True,null=True)
    max_setence = models.CharField(max_length=250,blank=True,null=True)
    a_f = models.CharField(max_length=250,blank=True,null=True,verbose_name="Age Factor")
    m_f = models.CharField(max_length=250,blank=True,null=True,verbose_name="M factor")
    keywords = models.TextField(max_length=1000, blank=True,unique=False, verbose_name="keywords")
    plead = models.CharField(max_length=250,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)

    class Meta:
         db_table = "law_inner_category"
         verbose_name_plural = "Sub law category"

    def __str__(self):
        return self.name