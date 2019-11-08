from rest_framework import serializers
from library.models import Book, BookItem, Swap, Wishlist
from user.serializers import DjangoUserSerializer, UserSerializerForBooksOwners, UserSerializer


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
    owner = UserSerializerForBooksOwners()

    class Meta:
        model = BookItem
        fields = ('status', 'owner', 'id', 'image')


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


class WishlistSerializerList(serializers.ModelSerializer):
    book = BookSerializerList()

    class Meta:
        model = Wishlist
        fields = ('book', 'created_at', 'id')