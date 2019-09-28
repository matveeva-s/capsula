from rest_framework import serializers
from library.models import Book, BookItem


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
