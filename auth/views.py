from django.contrib.auth import authenticate
from django.contrib.auth.models import User as DjangoUser
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json

from auth.forms import UserAuthForm, DjangoUserAuthForm


class LoginView(generics.RetrieveAPIView):
#todo exceptions
    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
            username = data['username']
            password = data['password']
        else:
            username = request.data['username']
            password = request.data['password']
        auth_user = authenticate(username=username, password=password)
        token = Token.objects.get_or_create(user=auth_user)
        resp = JsonResponse({'token': token[0].key})
        resp['Access-Control-Allow-Origin'] = '*'
        return resp



@permission_classes([IsAuthenticated])
class LogoutView(generics.RetrieveAPIView):
    queryset = DjangoUser.objects.all()

    def get(self, request, *args, **kwargs):
        token = request.headers['Authorization'][6:]
        user = Token.objects.get(key=token).user
        Token.objects.get(key=token).delete()
        Session.objects.all().delete() #todo ОЧЕНЬ плохоре решение, нужно удалять только текущую сессию
        return JsonResponse({})


class RegistrationView(generics.RetrieveAPIView):

    def post(self, request, *args, **kwargs):
        django_form = DjangoUserAuthForm(request.data)
        user_form = UserAuthForm(request.data)
        if django_form.is_valid() and user_form.is_valid():
            try:
                django_user = DjangoUser.objects.create_user(username=request.data['username'])
                django_user.set_password(request.data['password'])
                django_user.save()
            except Exception:
                return JsonResponse({'msg': 'Ошибка создания пользователя'}, status=400)

            user = user_form.save()
            user.django_user = django_user
            user.save()
            return JsonResponse({})
        else:
            if DjangoUser.objects.filter(username=request.data['username']).exists():
                return JsonResponse({'msg': 'Пользователь с таким именем уже существует'}, status=409)
            return JsonResponse({'msg': 'Ошибка создания, проверьте данные'}, status=400)
