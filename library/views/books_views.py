from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from django.http import JsonResponse

from management.models import ComplaintBook
from map.models import GeoPoint
from user.models import User
from library.models import Book, BookItem, Wishlist
from library.serializers import BookSerializerList, BookItemSerializerDetail, BookSerializerDetail, \
    BookItemSerializerList
from library.forms import BookItemForm
from capsula.utils import upload_file, get_user_from_request, delete_file, complete_headers, get_books, haversine
from capsula.settings.common import MEDIA_URL
from elastic_app.viewsets import book_search
from elastic_app.serializers import book_search_serializer


class BookListView(generics.RetrieveAPIView):
    serializer_class = BookSerializerList
    queryset = Book.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        genre = request.GET.get('genre')
        page_number = request.GET.get('page')
        search_results = Book.objects.all()
        if q and genre:
            search_results = book_search(q=q, genre=genre)
        elif q:
            search_results = book_search(q=q)
        elif genre:
            search_results = book_search(genre=genre)
        paginate_by = 20
        if search_results.count() % paginate_by == 0:
            page_counter = search_results.count() // paginate_by
        else:
            page_counter = search_results.count() // paginate_by + 1
        paginator = Paginator(search_results, paginate_by)
        page_number = request.GET.get('page')
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        data = book_search_serializer(page)
        return JsonResponse({'books': data, 'pages': page_counter})


@permission_classes([IsAuthenticated])
class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializerDetail
    queryset = BookItem.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        book_id = self.kwargs['id']
        book = get_object_or_404(Book, pk=book_id)
        book_items = BookItem.objects.filter(book=book).exclude(owner=user)
        serializer = self.get_serializer(book)
        serializer_items = BookItemSerializerList(book_items, many=True)
        book_items_list = serializer_items.data
        if request.GET.get('longitude'):
            longitude = float(request.GET.get('longitude')) #todo  проверка
        else:
            longitude = None
        if request.GET.get('latitude'):
            latitude = float(request.GET.get('latitude'))
        else:
            latitude = None
        if latitude is not None and longitude is not None:
            geo = True
        else:
            geo = False
        for book_item in book_items_list:
            geo_points = GeoPoint.objects.filter(user=book_item['owner']['id'])
            if len(geo_points):
                points = []
                for p in geo_points:
                    if geo:
                        distance = haversine(longitude, latitude, p.longitude, p.latitude)
                    else:
                        distance = None
                    points.append({'distance': distance, 'longitude': p.longitude, 'latitude': p.latitude})
                if geo:
                    points.sort(key=lambda x: x['distance'])
                    book_item['point'] = points[0]
                else:
                    book_item['point'] = points
                book_item['geolocationNotNull'] = True
            else:
                book_item['geolocationNotNull'] = False
                book_item['point'] = {}

        if len(Wishlist.objects.filter(book=book, user=user)) == 0:
            wishlist = {'added': False, 'id': None}
        else:
            wishlist = {'added': True, 'id': Wishlist.objects.get(book=book, user=user).id}
        complaint = True if len(ComplaintBook.objects.filter(book=book,
                                                            author=user,
                                                            status=ComplaintBook.NEW)) > 0 else False
        return Response({**serializer.data, **{'wishlist': wishlist,
                                              'book_items': book_items_list,
                                              'image': book.image,
                                              'complaint': complaint}})


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
        book_item = get_object_or_404(BookItem, pk=book_id)
        book = book_item.book
        if book_item.owner != user:
            return JsonResponse({'detail': 'Пользователь может редактировать только свои книги'}, status=403)
        # How to validate every field?
        # How to change field on abstr book AND in book_item?
        if data.get('title'):
            book.title = data.get('title')
        if data.get('genre'):
            book.genre = data.get('genre')
        if data.get('authors'):
            book.authors = data.get('authors')
        if data.get('status'):
            book_item.status = data.get('status')
        if data.get('isbn'):
            book_item.isbn = data.get('isbn')
        if data.get('image'):
            upload_file('books/{}/{}.jpg'.format(user.id, book_item.id), data.get('image'))
            book_item.image = MEDIA_URL + 'books/{}/{}.jpg'.format(user.id, book_item.id)
        book.save()
        book_item.save()
        return JsonResponse({})

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
        # todo: validation throuth forms
        title = data['title']
        authors = data['authors']
        genre = data['genre']
        existing_books = Book.objects.filter(title__contains=title, authors__contains=authors)
        if existing_books:
            book = existing_books[0]
        else:
            book = Book(title=title, authors=authors, genre=genre)
            book.save()
        book_item = BookItem.objects.create(book=book, owner=user)
        if data.get('image'):
            path = 'books/{}/{}.jpg'.format(user.id, book_item.id)
            if data.get('image').find('data:image') != -1:
                image = data['image']
                upload_file(path, image)
                book_item.image = MEDIA_URL + path
                if not book.image:
                    book.image = MEDIA_URL + path
                    book.save()
                book_item.save()
            else:
                book_item.image = data['image']
                if not book.image:
                    book.image = MEDIA_URL + path
                    book.save()
                book_item.save()
        if data.get('isbn'):
            book_item.isbn = data['isbn']
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
