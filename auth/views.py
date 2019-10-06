from django.contrib.auth.models import User as DjangoUser
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json

from auth.forms import UserAuthForm, DjangoUserAuthForm
from user.models import User
from user.serializers import UserSerializer


class LoginView(generics.RetrieveAPIView):
#todo exceptions + сессии
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
            username = data['username']
            password = data['password']
        else:
            username = request.data['username']
            password = request.data['password']
        auth_user = DjangoUser.objects.get(username=username)
        if auth_user and auth_user.check_password(password):
            request.session['member_id'] = auth_user.username
        else:
            resp = JsonResponse({'msg': 'Ошибка входа'}, status=401)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        token = Token.objects.get_or_create(user=auth_user)
        user = User.objects.get(django_user=auth_user)
        resp = JsonResponse({'token': token[0].key,
                             'username': auth_user.username,
                            'last_name': user.last_name,
                            'first_name': user.first_name,
                            'email': user.email})
        resp['Access-Control-Allow-Origin'] = '*'
        return resp



@permission_classes([IsAuthenticated])
class LogoutView(generics.RetrieveAPIView):
    queryset = DjangoUser.objects.all()

    def get(self, request, *args, **kwargs):
        token = request.headers['Authorization'][6:]
        user = Token.objects.get(key=token).user
        Token.objects.get(key=token).delete()
        try:
            del request.session['member_id']
        except KeyError:
            pass
        return JsonResponse({})


class RegistrationView(generics.RetrieveAPIView):

    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
            django_form = DjangoUserAuthForm(data)
            user_form = UserAuthForm(data)
        else:
            django_form = DjangoUserAuthForm(request.data)
            user_form = UserAuthForm(request.data)
        if django_form.is_valid() and user_form.is_valid():
            try:
                if request.content_type == 'text/plain;charset=UTF-8':
                    django_user = DjangoUser.objects.create_user(username=data['username'])
                    django_user.set_password(data['password'])
                else:
                    django_user = DjangoUser.objects.create_user(username=request.data['username'])
                    django_user.set_password(request.data['password'])
                django_user.save()
            except Exception:
                resp = JsonResponse({'msg': 'Ошибка создания пользователя'}, status=400)
                resp['Access-Control-Allow-Origin'] = '*'
                return resp
            user = user_form.save()
            user.django_user = django_user
            user.save()
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:#todo проверка почты
            if request.content_type == 'text/plain;charset=UTF-8':
                if DjangoUser.objects.filter(username=data['username']).exists():
                    resp = JsonResponse({'msg': 'Пользователь с таким именем уже существует'}, status=409)
                    resp['Access-Control-Allow-Origin'] = '*'
                    return resp
            else:
                if DjangoUser.objects.filter(username=request.data['username']).exists():
                    resp = JsonResponse({'msg': 'Пользователь с таким именем уже существует'}, status=409)
                    resp['Access-Control-Allow-Origin'] = '*'
                    return resp
            resp = JsonResponse({'msg': 'Ошибка создания, проверьте данные'}, status=400)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp