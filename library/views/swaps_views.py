from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.authtoken.models import Token

from library.models import Swap, BookItem
from library.serializers import SwapSerializerList, SwapSerializerDetail
from library.forms import SwapForm
from user.models import User


@permission_classes([IsAuthenticated])
class SwapListView(generics.RetrieveAPIView):
    serializer_class = SwapSerializerList
    queryset = Swap.objects.all()

    def get(self, request, *args, **kwargs):
        token = request.headers['Authorization'][6:]
        django_user = Token.objects.get(key=token).user
        user = User.objects.get(django_user=django_user)
        swaps_reader = Swap.objects.filter(reader=user)
        swaps_owner = Swap.objects.filter(book__owner=user)
        serializer_owner = self.get_serializer(swaps_owner, many=True)
        serializer_reader = self.get_serializer(swaps_reader, many=True)
        resp = Response({**{'owner': serializer_owner.data}, **{'reader': serializer_reader.data}})
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        form = SwapForm(data)
        if form.is_valid():
            bookitem = BookItem.objects.get(id=data["book_id"])
            if bookitem.status == BookItem.AVAILABLE:
                token = request.headers['Authorization'][6:]
                django_user = Token.objects.get(key=token).user
                user = User.objects.get(django_user=django_user)
                swap = Swap.objects.create(book=bookitem, reader=user, status=Swap.CONSIDERED)
                swap.save()
            elif bookitem:
                resp = JsonResponse({'msg': 'Книга недоступна'}, status=403)
                resp['Access-Control-Allow-Origin'] = '*'
                return resp
            else:
                resp = JsonResponse({'msg': 'Книга не найдена'}, status=404)
                resp['Access-Control-Allow-Origin'] = '*'
                return resp
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = JsonResponse({'msg': 'Ошибка создания, проверьте данные'}, status=400)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp


@permission_classes([IsAuthenticated])
class SwapDetailView(generics.ListCreateAPIView):
    serializer_class = SwapSerializerDetail
    queryset = Swap.objects.all()

    def get(self, request, *args, **kwargs):
        swap_id = self.kwargs['id']
        try:
            swap = Swap.objects.get(id=swap_id)
        except Exception:
            resp = JsonResponse({'msg': 'Заявка не найдена'}, status=404)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        token = request.headers['Authorization'][6:]
        django_user = Token.objects.get(key=token).user
        user = User.objects.get(django_user=django_user)
        if (swap.reader != user) and (swap.book.owner != user):
            resp = JsonResponse({'msg': 'Заявка недоступна для просмотра'}, status=403)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        serializer = self.get_serializer(swap)
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
        swap_id = self.kwargs['id']
        try:
            swap = Swap.objects.get(id=swap_id)
        except Exception:
            resp = JsonResponse({'msg': 'Заявка не найдена'}, status=404)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        if swap.book.owner == user and swap.status == Swap.CONSIDERED:
            if data['status'] == Swap.REJECTED:
                swap.status = data['status']
                swap.save()
            elif data['status'] == Swap.ACCEPTED:
                swap.book.status = BookItem.READING
                swap.book.save()
                swap.status = data['status']
                swap.save()
            else:
                resp = JsonResponse({'msg': 'Изменение запрещено'}, status=403)
                resp['Access-Control-Allow-Origin'] = '*'
                return resp
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        if swap.book.owner == user and swap.status == Swap.READING and data['status'] == Swap.RETURNED:
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
        resp = JsonResponse({'msg': 'Изменение запрещено'}, status=403)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def delete(self, request, *args, **kwargs):
        token = request.headers['Authorization'][6:]
        django_user = Token.objects.get(key=token).user
        user = User.objects.get(django_user=django_user)
        swap_id = self.kwargs['id']
        swap = Swap.objects.get(id=swap_id)
        if swap.reader == user and swap.status == Swap.CONSIDERED:
            Swap.objects.get(id=swap_id).delete()
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = JsonResponse({'msg': 'Невозможно удалить заявку'}, status=403)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp

