from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import django_filters.rest_framework
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from user.models import User
from library.models import Book, BookItem
from library.serializers import BookSerializerList, BookItemSerializerDetail, BookSerializerDetail, \
    BookItemSerializerList
from library.forms import BookItemForm
from capsula.utils import upload_file, get_user_from_request, delete_file, complete_headers
from capsula.settings.common import MEDIA_URL


#@permission_classes([IsAuthenticated])
class BookListView(generics.RetrieveAPIView):
    serializer_class = BookSerializerList
    queryset = Book.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['title', 'authors', 'genre']

    @complete_headers
    def get(self, request, *args, **kwargs):
        title = self.request.query_params.get('title', None)
        if title is not None:
            books = Book.objects.all().filter(title__contains=title)
        else:
            books = Book.objects.all()
        authors = self.request.query_params.get('authors', None)
        if authors is not None:
            books = books.filter(authors__contains=authors)
        genre = self.request.query_params.get('genre', None)
        if genre is not None:
            books = books.filter(genre=genre)
        #serializer = self.get_serializer(books, many=True)
        data = []
        for book in books:
            item = {}
            item['title'] = book.title
            item['authors'] = book.authors
            item['genre'] = book.genre
            item['id'] = book.id
            data.append({'book': item, 'image': BookItem.objects.filter(book=book)[0].image})
        return Response(data)


@permission_classes([IsAuthenticated])
class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializerDetail
    queryset = BookItem.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        book_id = self.kwargs['id']
        book = get_object_or_404(Book, pk=book_id)
        book_items = BookItem.objects.filter(book=book)
        image = book_items[0].image
        book_items = book_items.exclude(owner=user)
        serializer = self.get_serializer(book)
        serializer_items = BookItemSerializerList(book_items, many=True)
        return Response({**serializer.data, **{'book_items': serializer_items.data, 'image': image}})


@permission_classes([IsAuthenticated])
class BookItemsDetailView(generics.RetrieveAPIView):
    serializer_class = BookItemSerializerDetail
    queryset = BookItem.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['id']
        book = get_object_or_404(BookItem, pk=book_id)
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    @complete_headers
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
            return JsonResponse({'detail': 'Пользователь может редактировать только свои книги'}, status=403)
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
            return JsonResponse({})
        else:
            return JsonResponse({'detail': 'Ошибка создания, проверьте данные'}, status=400)

    @complete_headers
    def delete(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        book_id = self.kwargs['id']
        book = get_object_or_404(BookItem, pk=book_id)
        if book.owner != user:
            return JsonResponse({'detail': 'Пользователь может удалять только свои книги'}, status=403)
        else:
            abstract_book = get_object_or_404(BookItem, pk=book_id).book
            get_object_or_404(BookItem, pk=book_id).delete()
            if len(BookItem.objects.filter(book=abstract_book)) == 0:
                abstract_book.delete()
            if book.image:
                delete_file('books/{}/{}.jpg'.format(user.id, book_id))
            return JsonResponse({})


@permission_classes([IsAuthenticated])
class BookItemsListView(generics.ListCreateAPIView):
    serializer_class = BookItemSerializerDetail
    queryset = BookItem.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        owner = get_user_from_request(request)
        books = BookItem.objects.filter(owner=owner)
        data = []
        for book in books:
            serializer = self.get_serializer(book)
            book_data = serializer.data
            book_data['image'] = book.image
            data.append(book_data)
        return Response(data)

    @complete_headers
    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        user = get_user_from_request(request)
        #todo: validation throuth forms
        title = data['title']
        authors = data['authors']
        genre = data['genre']
        existing_books = Book.objects.filter(title__contains=title, authors__contains=authors)
        if existing_books:
            book = existing_books[0]
        else:
            book = Book.objects.create(title=title, authors=authors, genre=genre)
        book_item = BookItem.objects.create(book=book, owner=user)
        if request.data['image']:
            image = request.data['image']
            path = 'books/{}/{}.jpg'.format(user.id, book_item.id)
            upload_file(path, image)
            book_item.image = MEDIA_URL + path
            book_item.save()
        serializer = self.get_serializer(book_item)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
@complete_headers
def get_other_user_books_list(request, id):
    if request.method == 'GET':
        owner = get_object_or_404(User, pk=id)
        books = BookItem.objects.filter(owner=owner)
        data = []
        for book in books:
            serializer = BookItemSerializerDetail(book)
            book_data = serializer.data
            book_data['image'] = book.image
            data.append(book_data)
        return JsonResponse({'data': data})
