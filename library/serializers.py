from rest_framework import serializers
from library.models import Book, BookItem, Swap
from user.serializers import DjangoUserSerializer, UserShortSerializer, UserSerializer


class BookSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'authors', 'genre', 'id')


class BookItemSerializerDetail(serializers.ModelSerializer):
    book = BookSerializerList()

    class Meta:
        model = BookItem
        fields = ('book', 'status', 'id')


class BookSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'authors', 'genre', 'description', 'id')


class BookItemSerializerList(serializers.ModelSerializer):
    owner = UserShortSerializer()

    class Meta:
        model = BookItem
        fields = ('status', 'owner', 'id')


class SwapSerializerList(serializers.ModelSerializer):
    book = BookItemSerializerDetail()

    class Meta:
        model = Swap
        fields = ('book', 'status', 'id')


class SwapSerializerDetail(serializers.ModelSerializer):
    reader = UserSerializer()
    book = BookItemSerializerDetail()

    class Meta:
        model = Swap
        fields = ('book', 'reader', 'status', 'id')
