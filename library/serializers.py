from rest_framework import serializers
from library.models import Book, BookItem, Swap
from user.serializers import DjangoUserSerializer, UserSwapSerializer, UserSerializer


class BookSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'authors')


class BookItemSerializerList(serializers.ModelSerializer):
    book = BookSerializerList()

    class Meta:
        model = BookItem
        fields = ('book', 'status')


class BookSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'authors', 'genre', 'description')


class BookItemSerializerDetail(serializers.ModelSerializer):
    book = BookSerializerDetail()

    class Meta:
        model = BookItem
        fields = ('book', 'status')


class SwapSerializerList(serializers.ModelSerializer):
    book = BookItemSerializerList()

    class Meta:
        model = BookItem
        fields = ('book', 'status')


class SwapSerializerDetail(serializers.ModelSerializer):
    reader = UserSerializer()
    book = BookItemSerializerDetail()

    class Meta:
        model = Swap
        fields = ('book', 'reader', 'status')
