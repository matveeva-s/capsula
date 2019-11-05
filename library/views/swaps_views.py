from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json

from library.models import Swap, BookItem
from library.serializers import SwapSerializerList, SwapSerializerDetail
from capsula.utils import get_user_from_request, complete_headers


@permission_classes([IsAuthenticated])
class RequestsListView(generics.ListCreateAPIView):
    serializer_class = SwapSerializerList
    queryset = Swap.objects.all()

    @complete_headers
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
            data['book'] = {'title': swap.book.book.title, 'id': swap.book.book.id, 'status': swap.book.status}
            data['authors'] = swap.book.book.authors
            data['genre'] = swap.book.book.genre
            data['status'] = swap.status
            data['reader'] = {'name': '{} {}'.format(swap.reader.first_name, swap.reader.last_name),
                              'id': swap.reader.id, 'vk': swap.reader.contact, 'email': swap.reader.email}
            data['date'] = swap.updated_at.strftime('%d.%m.%Y')
            data['image'] = swap.book.image
            data_owner.append(data)
        for swap in swaps_reader:
            data = {}
            data['id'] = swap.id
            data['book'] = {'title': swap.book.book.title, 'id': swap.book.book.id, 'status': swap.book.status}
            data['authors'] = swap.book.book.authors
            data['genre'] = swap.book.book.genre
            data['status'] = swap.status
            data['owner'] = {'name': '{} {}'.format(swap.book.owner.first_name, swap.book.owner.last_name),
                             'id': swap.book.owner.id, 'vk': swap.book.owner.contact, 'email': swap.book.owner.email}
            data['date'] = swap.updated_at.strftime('%d.%m.%Y')
            data['image'] = swap.book.image
            data_reader.append(data)
        return JsonResponse({'owner': data_owner, 'reader': data_reader})

    @complete_headers
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
            return JsonResponse({'detail': 'Книга недоступна'}, status=403)
        else:
            return JsonResponse({'detail': 'Книга читается другим пользователем'}, status=403)


@permission_classes([IsAuthenticated])
class SwapDetailView(generics.ListCreateAPIView):
    serializer_class = SwapSerializerDetail
    queryset = Swap.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        swap_id = self.kwargs['id']
        swap = get_object_or_404(Swap, pk=swap_id)
        user = get_user_from_request(request)
        if (swap.reader != user) and (swap.book.owner != user):
            return JsonResponse({'detail': 'Заявка недоступна для просмотра'}, status=403)
        data = {}
        data['id'] = swap.id
        data['book'] = swap.book.book.title
        data['authors'] = swap.book.book.authors
        data['genre'] = swap.book.book.genre
        data['owner'] = '{} {}'.format(swap.book.owner.first_name, swap.book.owner.last_name)
        data['date'] = swap.updated_at.strftime('%d.%m.%Y')
        data['image'] = swap.book.image
        return JsonResponse(data)

    @complete_headers
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
                swap.updated_at = timezone.localtime()
                swap.save()
            elif data['status'] == Swap.ACCEPTED:
                swap.book.status = BookItem.READING
                swap.book.save()
                swap.status = data['status']
                swap.updated_at = timezone.localtime()
                swap.save()
            return JsonResponse({})
        elif swap.reader == user and swap.status == Swap.CONSIDERED: # поменять потом на CANCELED
            swap.status = data['status']
            swap.updated_at = timezone.localtime()
            swap.save()
            return JsonResponse({})
        elif swap.book.owner == user and swap.status == Swap.READING and data['status'] == Swap.RETURNED:
            swap.status = data['status']
            swap.updated_at = timezone.localtime()
            swap.save()
            return JsonResponse({})
        if swap.reader == user and swap.status == Swap.ACCEPTED and data['status'] == Swap.READING:
            swap.status = data['status']
            swap.updated_at = timezone.localtime()
            swap.save()
            return JsonResponse({})
        return JsonResponse({'detail': 'Изменение запрещено'}, status=403)

    @complete_headers
    def delete(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        swap_id = self.kwargs['id']
        swap = get_object_or_404(Swap, pk=swap_id)
        if swap.reader == user and swap.status == Swap.CONSIDERED:
            swap.delete()
            return JsonResponse({})
        else:
            return JsonResponse({'detail': 'Невозможно удалить заявку'}, status=403)

