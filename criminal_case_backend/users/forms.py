from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        # fields = ('name', 'email','role','attorney_no','profile_image','age_group','mobile','city','country','address')
        # fields = ('name', 'email','role','country','address')
        fields = '__all__'

class UserChangeForm(UserChangeForm):
	manual_activation = forms.BooleanField()
	class Meta:
		model = User
		# fields = ('email',)
		fields = '__all__'

	def clean(self):
		manual_activation = self.cleaned_data.pop('manual_activation', False)  
		if manual_activation:
			# send_email logics
			print("here")

		return self.cleaned_data
