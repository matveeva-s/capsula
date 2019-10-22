from rest_framework import serializers
from user.models import User
from django.contrib.auth.models import User as DjangoUser


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ('username', )


class UserSerializer(serializers.ModelSerializer):
    django_user = DjangoUserSerializer()

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'id', 'django_user', 'location', 'contact', 'image')


class UserShortSerializer(serializers.ModelSerializer):
    django_user = DjangoUserSerializer()

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'django_user')


class UserSerializerForBooksOwners(serializers.ModelSerializer):
    django_user = DjangoUserSerializer()

    class Meta:
        model = User
        fields = ('id', 'django_user')
