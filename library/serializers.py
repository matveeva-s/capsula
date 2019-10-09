from rest_framework import serializers
from library.models import Book, BookItem, Swap
from user.serializers import DjangoUserSerializer


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


class SwapSerializer(serializers.ModelSerializer):
    book = BookSerializerDetail()
    owner = DjangoUserSerializer()

    class Meta:
        model = BookItem
        fields = ('book', 'status', 'owner')


class SwapSerializerDetail(serializers.ModelSerializer):
    reader = DjangoUserSerializer()
    book = SwapSerializer()

    class Meta:
        model = Swap
        fields = ('book', 'reader', 'status')
