from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]

    )
    password2=serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model=User
        fields=[
            'usernmae',
            'email',
            'password',
            'password2',
            'role',
            'phone',

        ]
    def validate(self,attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError(
                {
                    'password':'Passwords do not match'
                }
            )
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('password2')
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get['role','candidate'],
            phone=validated_data.get['phone','']
            
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            'id',
            'username',
            'email',
            'role',
            'phone',
            'profile_picture',
            'is_email_verified',
            'created_at',
        ]
        read_only_fields=[
            'id',
            'is_email_verified',
            'created_at'
        ]

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True,write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(
        required=True,
        write_only=True
    )
    new_password=serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password2=serializers.CharField(
        required=True,
        write_only=True,
        
    )
    def validate(self,attrs):
        if attrs['new_password']!=attrs['new_password2']:
            raise serializers.ValidationError(
                {
                    'new_password':'Passwords do not match'
                }
            )
        return attrs
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            'email',
            'phone',
            'profile_picture',
            'first_name',
            'last_name',



        ]




           



     


    