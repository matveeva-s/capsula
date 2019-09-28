from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.http import JsonResponse
from user.models import User
from library.models import BookItem, Book
from user.serializers import UserSerializer
from library.serializers import BookItemSerializerList, BookItemSerializerDetail
from user.forms import BookForm


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserBookListView(generics.ListCreateAPIView):
    serializer_class = BookItemSerializerList
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['pk'])
        books = self.queryset.filter(owner=user)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['pk'])
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.data['title']
            authors = form.data['authors']
            existing_books = Book.objects.filter(title__contains=title, authors__contains=authors)
            if existing_books:
                book = existing_books[0]
            else:
                book = form.save()
            book_item = BookItem.objects.create(book=book, owner=user)
            book_item.save()
            return JsonResponse({})
        else:
            return JsonResponse({'msg': 'Ошибка создания, проверьте данные'}, status=400)


class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookItemSerializerDetail
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['id']
        book = BookItem.objects.get(id=book_id)
        serializer = self.get_serializer(book)
        return Response(serializer.data)



