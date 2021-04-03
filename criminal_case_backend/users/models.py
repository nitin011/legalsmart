from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from criminal_case_backend.base.models import  TimeStampedUUIDModel, UUIDModel

from .managers import UserManager

from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.EmailField(_('username'), unique=False, blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(default='user',max_length=200,blank=True)
    token = models.CharField(default='',max_length=200,blank=True)
    attorney_no = models.CharField(max_length=255,blank=True,null=True,verbose_name="Attorney No")
    age_group = models.CharField(max_length=120, null=True, blank=False, verbose_name="Age Group") #help_text='Designates whether the user is Attorney or Juror.')

    # Profile Image
    profile_image = models.ImageField(upload_to = "profileImages",blank=True,null=True,default = '', verbose_name="Profile Image")
    
    mobile = models.CharField(max_length=200,blank=False,null=True,unique=True)
    city = models.CharField(max_length=200,blank=True)
    name = models.CharField(max_length=200,blank=False)
    first_name = models.CharField(max_length=200,blank=False)
    last_name = models.CharField(max_length=200,blank=False)
    country = models.CharField(max_length=200,blank=True)
    address = models.CharField(max_length=200,blank=True)
    device_id = models.CharField(max_length=300,blank=True, null=True)
    os_type = models.CharField(max_length=200,blank=True, null=True)
    fcm_token = models.CharField(max_length=200,blank=True, null=True)
    user_locations = models.CharField(max_length=200,blank=True, null=True)
    user_access = models.CharField(max_length=200,blank=True, null=True)
    bar_number = models.CharField(max_length=200,blank=True, null=True)
    year_of_practise = models.CharField(max_length=200,blank=True, null=True)
    area_of_interest = models.CharField(max_length=200,blank=True, null=True)
    court_preference = models.CharField(max_length=200,blank=True, null=True)
    court_preference1 = models.CharField(max_length=200,blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def activate_user(sender, instance=None, created=False, **kwargs):
#     if is_active:
#         email = EmailMessage("account activated", "hi", to=[to_email])
#         email.send()
#         return HttpResponse('We have sent you an email')

# Create your models here.
class Roles(TimeStampedUUIDModel):
    USER_ROLE = (
        ('attorney', 'attorney'),
        ('juror', 'juror'),
        ('user', 'user'),
        ('judge', 'judge')
    )

    role = models.CharField(max_length=120, null=False, blank=False, choices=USER_ROLE, help_text='Designates whether the user')

    def __str__(self):
        return self.role 

    class Meta:
        # pass
        db_table = "user_roles"
        verbose_name = ('Roles')
        verbose_name_plural = ('Roles')

class GeoLocations(TimeStampedUUIDModel):
    name = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user_geo_locations"
        # verbose_name = ('App Locations')
        # verbose_name_plural = ('App Locations')

class ProfileLocations(TimeStampedUUIDModel):
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(GeoLocations, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user_profile_locations"
        # verbose_name = ('User Profile Location')
        # verbose_name_plural = ('User Profile Location')

class Access(TimeStampedUUIDModel):
    name = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "profile_access"
        verbose_name = ('Profile Access')
        verbose_name_plural = ('Profile Access')

class ProfileAccess(TimeStampedUUIDModel):
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    access = models.ForeignKey(Access, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        # pass
        db_table = "user_profile_access"
        verbose_name = ('User Profile Access')
        verbose_name_plural = ('User Profile Access')

class GeoLocations1(models.Model):
    name = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user_geo_location"
        verbose_name = ('App Locations')
        verbose_name_plural = ('App Locations')

class Access1(models.Model):
    name = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user_profile_access1"
        verbose_name = ('Profile Access')
        verbose_name_plural = ('Profile Access')

class AreaOfInterest(models.Model):
    name = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        # pass
        db_table = "area_of_interest"
        verbose_name = ('Area Of Interest')
        verbose_name_plural = ('Area Of Interest')

class WiPayPayment(models.Model):
    phone = models.CharField(max_length=200, blank=True)
    total = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)
    order_id = models.CharField(max_length=200, blank=True)
    return_url = models.CharField(max_length=200, blank=True)
    reasonCode = models.CharField(max_length=200, blank=True)
    reasonDescription = models.CharField(max_length=2000, blank=True)
    responseCode = models.CharField(max_length=200, blank=True)
    order_hash =  models.CharField(max_length=200, blank=True)
    date = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        # pass
        db_table = "wipay_payment"
        verbose_name = ('Payments')
        verbose_name_plural = ('Payments')