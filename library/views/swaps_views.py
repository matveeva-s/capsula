from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.authtoken.models import Token
from library.models import Swap, BookItem
from library.serializers import SwapSerializerList
from library.forms import SwapForm
from user.models import User

@permission_classes([IsAuthenticated])
class SwapListlView(generics.RetrieveAPIView):
    serializer_class = SwapSerializerList
    queryset = Swap.objects.all()

    # todo придумать как возвращать не весь список а пачками по мере прогрузки
    def get(self, request, *args, **kwargs):
        swaps = Swap.objects.all()
        serializer = self.get_serializer(swaps, many=True)
        resp = Response(serializer.data)
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
    pass