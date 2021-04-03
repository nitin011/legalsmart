from rest_framework import serializers
from . import models
from criminal_case_backend.users.models import User, Locations

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'email','role','attorney_no','profile_image','age_group','mobile','city','country','address')
        # extra_kwargs = {'password': {'write_only': True} }

class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):
    # token = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(read_only=True)
  
    class Meta:
        model = User
        fields = ('name', 'email','role','mobile','age_group','password')
        # fields = ('id','email','password','token')
        # extra_kwargs = {'password': {'write_only': True} }
        read_only_fields = ('id',)

    # def create(self, validated_data):
    #     user = User(**validated_data)
    #     # user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data)
        # user.set_password(validated_data['password'])
        user.save()
        return user

class EmptySerializer(serializers.Serializer):
    pass


class UserProfileImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('profile_image',)
       
    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'email','role','attorney_no','age_group','mobile','city','country','address')
        # extra_kwargs = {'password': {'write_only': True} }


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    token = serializers.CharField(max_length=256)
    # email = serializers.CharField(max_length=128)
    # password = serializers.CharField(write_only=True,
    #                                  required=True,
    #                                  style={
    #                                      'input_type': 'password',
    #                                      'placeholder': 'password'
    #                                  })
    class Meta:
        model = User
        fields = ('email','token')

    # def create(self, validated_data):
    #     user = User(**validated_data)
    #     user.save()
        # return user


class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('longitute', 'latitude','device_id','user',)



# class UserProfileChangeSerializer(serializers.ModelSerializer):
#     username = CharField(required=False, allow_blank=True, initial="current username")
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'password',
#         ]

#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username',instance.username)
#         return instance 



    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     profile = instance.profile

    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()

    #     profile.title = profile_data.get('title', profile.title)
    #     profile.dob = profile_data.get('dob', profile.dob)
    #     profile.address = profile_data.get('address', profile.address)
    #     profile.country = profile_data.get('country', profile.country)
    #     profile.city = profile_data.get('city', profile.city)
    #     profile.zip = profile_data.get('zip', profile.zip)
    #     profile.save()

    #     return instance
