from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.utils import json

from library.models import Wishlist, BookItem, Book
from library.serializers import BookSerializerList
from capsula.utils import complete_headers, get_user_from_request


class WishlistView(generics.RetrieveAPIView):
    serializer_class = BookSerializerList
    queryset = Wishlist.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        wishlist = Wishlist.objects.filter(user=user)
        data_list = []
        for wish in wishlist:
            data = {}
            serializer = self.get_serializer(wish.book)
            book = serializer.data
            data['book'] = book
            book_items = BookItem.objects.filter(book=wish.book)
            image = book_items[0].image
            data['image'] = image
            data['created_at'] = wish.created_at.strftime('%d.%m.%Y')
            data['id'] = wish.id
            if len(BookItem.objects.filter(book=wish.book, status=BookItem.AVAILABLE)) != 0:
                data['available'] = True
            else:
                data['available'] = False
            data_list.append(data)
        return Response(data_list)

    @complete_headers
    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        user = get_user_from_request(request)
        book = get_object_or_404(Book, id=data['id'])
        if len(Wishlist.objects.filter(user=user, book=book)) == 0:
            Wishlist.objects.create(user=user, book=book)
        else:
            return JsonResponse({'detail': 'Книга уже есть в вашем вишлисте'}, status=409)
        id = Wishlist.objects.get(user=user, book=book).id
        return JsonResponse({'id': id}, status=200)


class WishlistDetailView(generics.RetrieveAPIView):

    @complete_headers
    def delete(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        wishlist_id = self.kwargs['id']
        wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
        if wishlist.user != user:
            return JsonResponse({'detail': 'Пользователь может удалять только свои книги'}, status=403)
        else:
            wishlist.delete()
            return JsonResponse({})
