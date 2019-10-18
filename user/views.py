from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.serializers import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.permissions import IsAuthenticated
from user.forms import UserForm
from user.models import User
from user.serializers import UserSerializer
from capsula.utils import upload_file
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

#todo шифровать пароль при регистрации и входе
@permission_classes([IsAuthenticated])
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        serializer = self.get_serializer(user)
        resp = Response(serializer.data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


@permission_classes([IsAuthenticated])
class MeDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        token = request.headers['Authorization'][6:]
        django_user = Token.objects.get(key=token).user
        user = User.objects.get(django_user=django_user)
        serializer = self.get_serializer(user)
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
        form = UserForm(data)
        if form.is_valid():
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            resp = Response()
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = JsonResponse({'msg': 'Ошибка создания, проверьте данные'}, status=400)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp


@permission_classes([IsAuthenticated])
class UserListView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        resp = Response(serializer.data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


@permission_classes([IsAuthenticated])
def change_avatar(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_avatar = request.FILES.get('image')
        upload_path = 'avatar/{}'.format(pk)
        upload_file(upload_path, user_avatar)
    return JsonResponse({})

