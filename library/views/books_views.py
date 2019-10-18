from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from user.models import User, DjangoUser
from library.models import Book, BookItem
from library.serializers import BookSerializerList, BookItemSerializerDetail, BookSerializerDetail, \
    BookItemSerializerList
from library.forms import BookForm, BookItemForm
from capsula.utils import upload_file, get_user_from_request, check_key_existing, get_b64str_from_path, delete_file


@permission_classes([IsAuthenticated])
class BookListView(generics.RetrieveAPIView):
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
        book = get_object_or_404(Book, pk=book_id)
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
        book = get_object_or_404(BookItem, pk=book_id)
        serializer = self.get_serializer(book)
        resp = Response(serializer.data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def put(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        user = get_user_from_request(request)
        form = BookItemForm(data)
        book_id = self.kwargs['id']
        book = get_object_or_404(BookItem, pk=book_id)
        if book.owner != user:
            resp = JsonResponse({'detail': 'Пользователь может редактировать только свои книги'}, status=403)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        # How to validate every field?
        # How to change field on abstr book AND in book_item?
        if form.is_valid():
            if data.get('title'):
                book.title = data.get('title')
            if data.get('genre'):
                book.genre = data.get('genre')
            if data.get('authors'):
                book.authors = data.get('authors')
            if data.get('status'):
                book.status = data.get('status')
            if data.get('isbn'):
                book.isbn = data.get('isbn')
            if data.get('image'):
                upload_file('books/{}/{}.jpg'.format(user.id, book.id), data.get('image'))
            book.save()
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = JsonResponse({'detail': 'Ошибка создания, проверьте данные'}, status=400)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp

    def delete(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        book_id = self.kwargs['id']
        book = get_object_or_404(BookItem, pk=book_id)
        if book.owner != user:
            resp = JsonResponse({'detail': 'Пользователь может удалять только свои книги'}, status=403)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            get_object_or_404(BookItem, pk=book_id).delete()
            delete_file('books/{}/{}.jpg'.format(user.id, book_id))
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp


@permission_classes([IsAuthenticated])
class BookItemsListView(generics.RetrieveAPIView):
    serializer_class = BookItemSerializerDetail
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        owner = get_user_from_request(request)
        books = BookItem.objects.filter(owner=owner)
        data = []
        for book in books:
            serializer = self.get_serializer(book)
            book_data = serializer.data
            file_path = 'books/{}/{}.jpg'.format(owner.id, book.id)
            if check_key_existing(file_path):
                book_data['image'] = get_b64str_from_path(file_path)
            data.append(book_data)
        resp = Response(data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        form = BookForm(data)
        user = get_user_from_request(request)
        if form.is_valid():
            title = form.data.get('title')
            authors = form.data.get('authors')
            existing_books = Book.objects.filter(title__contains=title, authors__contains=authors)
            if existing_books:
                book = existing_books[0]
            else:
                book = form.save()
            book_item = BookItem.objects.create(book=book, owner=user)
            image = request.FILES.get('image')
            if image:
                upload_file('books/{}/{}.jpg'.format(user.id, book_item.id), image)
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = JsonResponse({'detail': 'Ошибка создания, проверьте данные'}, status=400)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp


@permission_classes([IsAuthenticated])
def get_other_user_books_list(request, id):
    if request.method == 'GET':
        owner = get_object_or_404(User, pk=id)
        books = BookItem.objects.filter(owner=owner)
        data = []
        for book in books:
            serializer = BookItemSerializerDetail(book)
            book_data = serializer.data
            file_path = 'books/{}/{}.jpg'.format(owner.id, book.id)
            if check_key_existing(file_path):
                book_data['image'] = get_b64str_from_path(file_path)
            data.append(book_data)
        resp = JsonResponse({'data': data})
        resp['Access-Control-Allow-Origin'] = '*'
        return resp
