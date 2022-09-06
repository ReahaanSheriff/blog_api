from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate


class CreateBlogSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model = CreateBlog
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["created"]= instance.created.strftime("%d, %b %-y %-I:%M %p")
        data["username"] = instance.user_id_id.username
        data['short'] = instance.body[:50]
        return data


# Report Serializer
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    liked_list = CreateBlogSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'liked_list')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if User.objects.filter(email__iexact=validated_data['email'].lower()).exists():
            raise serializers.ValidationError("Duplicate email")
        else:
            user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")



class ChangePasswordSerializer(serializers.Serializer):

    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)