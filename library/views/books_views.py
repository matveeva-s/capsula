from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.authtoken.models import Token
from library.models import Book, BookItem
from library.serializers import BookSerializerList, BookItemSerializerDetail, BookSerializerDetail, \
    BookItemSerializerList
from library.forms import BookForm, BookItemForm
from user.models import User


@permission_classes([IsAuthenticated])
class BookListlView(generics.RetrieveAPIView):
    serializer_class = BookSerializerList
    queryset = Book.objects.all()

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = self.get_serializer(books, many=True)
        resp = Response(serializer.data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


@permission_classes([IsAuthenticated])
class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializerDetail
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['id']
        try:
            book = Book.objects.get(id=book_id)
        except Exception:
            resp = JsonResponse({'msg': 'Книга не найдена'}, status=404)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        book_items = BookItem.objects.filter(book=book)
        serializer = self.get_serializer(book)
        serializer_items = BookItemSerializerList(book_items, many=True)
        resp = Response({**serializer.data, **{'book_items': serializer_items.data}})
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


@permission_classes([IsAuthenticated])
class BookItemsDetailView(generics.RetrieveAPIView):
    serializer_class = BookItemSerializerDetail
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['id']
        try:
            book = BookItem.objects.get(id=book_id)
        except Exception:
            resp = JsonResponse({'msg': 'Книга не найдена'}, status=404)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        serializer = self.get_serializer(book)
        resp = Response(serializer.data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def put(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        token = request.headers['Authorization'][6:]
        django_user = Token.objects.get(key=token).user
        user = User.objects.get(django_user=django_user)
        form = BookItemForm(data)
        book_id = self.kwargs['id']
        book = BookItem.objects.get(id=book_id)
        if book.owner != user:
            resp = JsonResponse({'msg': 'Пользователь может редактировать только свои книги'}, status=403)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        if form.is_valid():
            if data['status']:
                book.status = data['status']
            if data['isbn']:
                book.isbn = data['isbn']
            book.save()
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = JsonResponse({'msg': 'Ошибка создания, проверьте данные'}, status=400)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp

    def delete(self, request, *args, **kwargs):
        token = request.headers['Authorization'][6:]
        django_user = Token.objects.get(key=token).user
        user = User.objects.get(django_user=django_user)
        book_id = self.kwargs['id']
        book = BookItem.objects.get(id=book_id)
        if book.owner != user:
            resp = JsonResponse({'msg': 'Пользователь может удалять только свои книги'}, status=403)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            BookItem.objects.get(id=book_id).delete()
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp


@permission_classes([IsAuthenticated])
class BookItemsListlView(generics.RetrieveAPIView):
    serializer_class = BookItemSerializerDetail
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        books = BookItem.objects.all()
        serializer = self.get_serializer(books, many=True)
        resp = Response(serializer.data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        form = BookForm(data)
        token = request.headers['Authorization'][6:]
        django_user = Token.objects.get(key=token).user
        user = User.objects.get(django_user=django_user)
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
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = JsonResponse({'msg': 'Ошибка создания, проверьте данные'}, status=400)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
