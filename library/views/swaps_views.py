from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json

from library.models import Swap, BookItem
from library.serializers import SwapSerializerList, SwapSerializerDetail
from capsula.utils import get_user_from_request, check_key_existing, get_b64str_from_path


@permission_classes([IsAuthenticated])
class RequestsListView(generics.ListCreateAPIView):
    serializer_class = SwapSerializerList
    queryset = Swap.objects.all()

    def get(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        swaps_reader = Swap.objects.filter(reader=user)
        swaps_owner = Swap.objects.filter(book__owner=user)
        data_owner = []
        data_reader = []
        # todo check times DB hitting and optimize with select_related
        for swap in swaps_owner:
            data = {}
            data['id'] = swap.id
            data['book'] = swap.book.book.title
            data['authors'] = swap.book.book.authors
            data['genre'] = swap.book.book.genre
            data['reader'] = '{} {}'.format(swap.reader.first_name, swap.reader.last_name)
            data['date'] = swap.created_at
            image_location_key = 'books/{}/{}.jpg'.format(user.id, swap.book.id)
            if check_key_existing(image_location_key):
                data['image'] = get_b64str_from_path(image_location_key)
            data_owner.append(data)
        for swap in swaps_reader:
            data = {}
            data['id'] = swap.id
            data['book'] = swap.book.book.title
            data['authors'] = swap.book.book.authors
            data['genre'] = swap.book.book.genre
            data['owner'] = '{} {}'.format(swap.book.owner.first_name, swap.book.owner.last_name)
            data['date'] = swap.created_at
            image_location_key = 'books/{}/{}.jpg'.format(swap.book.owner.id, swap.book.id)
            if check_key_existing(image_location_key):
                data['image'] = get_b64str_from_path(image_location_key)
            data_reader.append(data)
        resp = JsonResponse({'owner': data_owner, 'reader': data_reader})
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        bookitem = get_object_or_404(BookItem, pk=data["book_id"])
        if bookitem.status == BookItem.AVAILABLE:
            user = get_user_from_request(request)
            Swap.objects.create(book=bookitem, reader=user, status=Swap.CONSIDERED)
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        elif bookitem.status == BookItem.NOT_AVAILABLE:
            resp = JsonResponse({'detail': 'Книга недоступна'}, status=403)
        else:
            resp = JsonResponse({'detail': 'Книга читается другим пользователем'}, status=403)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


@permission_classes([IsAuthenticated])
class SwapDetailView(generics.ListCreateAPIView):
    serializer_class = SwapSerializerDetail
    queryset = Swap.objects.all()

    def get(self, request, *args, **kwargs):
        swap_id = self.kwargs['id']
        swap = get_object_or_404(Swap, pk=swap_id)
        user = get_user_from_request(request)
        if (swap.reader != user) and (swap.book.owner != user):
            resp = JsonResponse({'detail': 'Заявка недоступна для просмотра'}, status=403)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        data = {}
        data['id'] = swap.id
        data['book'] = swap.book.book.title
        data['authors'] = swap.book.book.authors
        data['genre'] = swap.book.book.genre
        data['owner'] = '{} {}'.format(swap.book.owner.first_name, swap.book.owner.last_name)
        data['date'] = swap.created_at
        image_location_key = 'books/{}/{}.jpg'.format(swap.book.owner.id, swap.book.id)
        if check_key_existing(image_location_key):
            data['image'] = get_b64str_from_path(image_location_key)
        resp = JsonResponse(data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def put(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        user = get_user_from_request(request)
        swap_id = self.kwargs['id']
        swap = get_object_or_404(Swap, pk=swap_id)
        if swap.book.owner == user and swap.status == Swap.CONSIDERED:
            if data['status'] == Swap.REJECTED:
                swap.status = data['status']
                swap.save()
            elif data['status'] == Swap.ACCEPTED:
                swap.book.status = BookItem.READING
                swap.book.save()
                swap.status = data['status']
                swap.save()
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        elif swap.book.owner == user and swap.status == Swap.READING and data['status'] == Swap.RETURNED:
            swap.status = data['status']
            swap.save()
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        if swap.reader == user and swap.status == Swap.ACCEPTED and data['status'] == Swap.READING:
            swap.status = data['status']
            swap.save()
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        resp = JsonResponse({'detail': 'Изменение запрещено'}, status=403)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def delete(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        swap_id = self.kwargs['id']
        swap = get_object_or_404(Swap, pk=swap_id)
        if swap.reader == user and swap.status == Swap.CONSIDERED:
            swap.delete()
            resp = JsonResponse({})
        else:
            resp = JsonResponse({'detail': 'Невозможно удалить заявку'}, status=403)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

