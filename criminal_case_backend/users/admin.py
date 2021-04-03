# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
# # Unregister the provided model admin
# admin.site.unregister(UserGroup)

# # Register out own model admin, based on the default UserAdmin
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     pass

# admin.site.unregister(Group)

from django.apps import apps

# # admin.site.register(User, UserAdmin)
# Bookmark
models = apps.get_models()

# for model in models:
# 	# print("=======================")
# 	# print(model)
# 	# if "User" in model:
# 	try:
# 		admin.site.register(model)
# 	except admin.sites.AlreadyRegistered:
# 		pass



from django.contrib import admin
# Need to import this since auth models get registered on import.
import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import auth
from .models import User

# admin.site.unregister(User)
admin.site.unregister(auth.models.Group)



from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User,WiPayPayment
from django import forms

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         exclude = ('username',)
#     # username = forms.EmailField(max_length=64, help_text="The person's email address.")
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         return email


# class UserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     form = UserChangeForm
#     model = User
#     list_display = ['email', 'name',]

# admin.site.register(User, UserAdmin)




# Third Party Stuff
# from django.conf import settings
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
# from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
# from django.contrib.admin.actions import delete_selected as admin_delete_selected
# from rangefilter.filter import DateTimeRangeFilter

# # Electric_Soul Stuff
# from electric_soul.auth import services
# from electric_soul.base.models import ElasticSearchWrapper
# from .models import User, UserActivationKey, UserFollow, Device


# # Forms
# # ----------------------------------------------------------------------------
# class MyUserCreationForm(DjangoUserCreationForm):
#     class Meta:
#         model = User
#         fields = ("email", "username")


# class MyUserChangeForm(DjangoUserChangeForm):
#     class Meta:
#         model = User
#         fields = '__all__'


# # ModelAdmins
# # ----------------------------------------------------------------------------
# @admin.register(User)
# class UserAdmin(AuthUserAdmin):
#     add_form_template = 'admin/auth/user/add_form.html'
#     model = User
#     fieldsets = (
#         (None, {'fields': ('email', 'username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'cover_image', 'country','role',)}),
#         ('Facebook info', {'fields': ('fb_id', 'fb_auth_token', 'fb_data', 'fb_invite_image')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                     'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'password1', 'password2'),
#         }),
#     )
#     readonly_fields = ('date_joined', 'last_login')
#     form = MyUserChangeForm
#     add_form = MyUserCreationForm
#     list_display = ('email', 'username', 'first_name', 'last_name','is_active')
#     list_filter = (('date_joined', DateTimeRangeFilter), 'is_superuser', 'is_active', 'country')
#     search_fields = ('first_name', 'last_name', 'email', 'username')
#     ordering = ('email', '-date_joined')
#     actions = ['delete_selected', 'resend_activation']



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Locations, GeoLocations1, ProfileLocations, Access1, ProfileAccess, AreaOfInterest, CourtPreference

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email','name','mobile', 'age_group', 'city', 'country','role','user_locations','fcm_token','is_active')
    list_filter = ('mobile', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('name','mobile', 'age_group', 'city', 'country','role', 'fcm_token')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','mobile', 'password1', 'password2', 'is_active','is_superuser')}
        ),
    )
    search_fields = ('email',)
    readonly_fields = ["fcm_token"]
    ordering = ('email',)

class LocationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude','longitude')
    list_display_links = ('id',)

class GeoLocations1Admin(admin.ModelAdmin):
    list_display = ('id', 'name','status')
    list_display_links = ('id',)

class AreaOfInterestAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'status')
    list_display_links = ('id',)

class CourtPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','status')
    list_display_links = ('id',)

class Access1Admin(admin.ModelAdmin):
    list_display = ('id', 'name','status')
    list_display_links = ('id',)

# GeoLocations, ProfileLocations, Access, ProfileAccess
admin.site.register(User, UserAdmin)
admin.site.register(Locations, LocationsAdmin)
admin.site.register(AreaOfInterest, AreaOfInterestAdmin)
admin.site.register(CourtPreference, CourtPreferenceAdmin)
admin.site.register(Access1, Access1Admin)
admin.site.register(GeoLocations1, GeoLocations1Admin)

class AttorneyUser(User):
    class Meta:
        proxy = True


def send_account_details(modeladmin, request, queryset):
    # Your email sending code here.
    # The queryset contains selected users
    print("I am here")
    return True

class AttorneyUserAdmin(UserAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(role = 'Attorney')

    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    # list_display = ('email','name','role',  'country','is_active')
    list_display = ('email','name','mobile', 'age_group','mobile', 'city', 'country','role','user_locations','fcm_token','is_active','bar_number')
    
    # list_filter = ('name', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('name', 'role', 'city','mobile', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2','role', 'is_active')}
        ),
    )
    # search_fields = ('email',)
    search_fields = ('username', 'name', 'email')
    # list_filter = ('state',)
    ordering = ('email',)
    actions = ['send_account_details']



admin.site.register(AttorneyUser, AttorneyUserAdmin)



class JudgeUser(User):
    class Meta:
        proxy = True

class JudgeUserAdmin(UserAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(role = 'judge')

    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    # list_display = ('email','name','role',  'country','is_active')
    list_display = ('email','name','mobile', 'age_group', 'city', 'country','role','user_locations','fcm_token','is_active','bar_number')
    
    # list_filter = ('name', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('name', 'role','mobile', 'city', 'country',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2','role', 'is_active')}
        ),
    )
    # search_fields = ('email',)
    search_fields = ('username', 'name', 'email')
    # list_filter = ('state',)
    ordering = ('email',)
    actions = ['send_account_details']



admin.site.register(JudgeUser, JudgeUserAdmin)

class WiPayPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'total','order_id','reasonDescription')
    list_display_links = ('id','name')

admin.site.register(WiPayPayment, WiPayPaymentAdmin)