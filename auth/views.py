from builtins import KeyError

from django.contrib.auth import logout
from django.contrib.auth.models import User as DjangoUser
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from social_django.models import UserSocialAuth

from auth.forms import UserAuthForm, DjangoUserAuthForm
from user.models import User
from user.serializers import UserSerializer


class LoginView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        username = data['username']
        password = data['password']
        auth_user = DjangoUser.objects.get(username=username)
        if auth_user and auth_user.check_password(password):
            request.session['member_id'] = auth_user.username
        else:
            resp = JsonResponse({'msg': 'Ошибка входа (проверьте логин и пароль)'}, status=401)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        token = Token.objects.get_or_create(user=auth_user)
        user = User.objects.get(django_user=auth_user)
        serializer = self.get_serializer(user)
        data = serializer.data
        data['image'] = user.avatar
        resp = JsonResponse({**{'token': token[0].key}, **data})
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            resp = JsonResponse({}, status=204)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            django_user = request.user
            user = User.objects.filter(django_user=django_user)
            if len(user) == 0:
                vk_user = UserSocialAuth.objects.get(user=django_user)
                user = User.objects.create(django_user=django_user,
                                           first_name=django_user.first_name,
                                           last_name=django_user.last_name,
                                           email= django_user.email,
                                           contact=vk_user.uid)
            else:
                user = User.objects.get(django_user=django_user)
            token = Token.objects.get_or_create(user=django_user)
            serializer = self.get_serializer(user)
            data = serializer.data
            data['image'] = user.avatar
            resp = JsonResponse({**{'token': token[0].key}, **data})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp


@permission_classes([IsAuthenticated])
class LogoutView(generics.RetrieveAPIView):
    queryset = DjangoUser.objects.all()

    def get(self, request, *args, **kwargs):
        token = request.headers['Authorization'][6:]
        user = Token.objects.get(key=token).user
        if user:
            Token.objects.get(key=token).delete()
            vk_user = UserSocialAuth.objects.filter(user=user)
            if len(vk_user) > 0:
                logout(request)
        try:
            del request.session['member_id']
        except KeyError:
            pass
        resp = JsonResponse({})
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


class RegistrationView(generics.RetrieveAPIView):

    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        django_form = DjangoUserAuthForm(data)
        user_form = UserAuthForm(data)
        if django_form.is_valid() and user_form.is_valid():
            django_user = DjangoUser.objects.create_user(username=data['username'])
            django_user.set_password(data['password'])
            django_user.save()
            user = user_form.save()
            user.django_user = django_user
            user.save()
            resp = JsonResponse({})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            if DjangoUser.objects.filter(username=data['username']).exists():
                resp = JsonResponse({'msg': 'Пользователь с таким именем уже существует'}, status=409)
                resp['Access-Control-Allow-Origin'] = '*'
                return resp
            if user_form.errors['email'][0] == 'User with this Email already exists.':
                resp = JsonResponse({'msg': 'Адрес электронной почты уже используется'}, status=409)
                resp['Access-Control-Allow-Origin'] = '*'
                return resp
            resp = JsonResponse({'msg': 'Ошибка создания, проверьте данные'}, status=400)
            resp['Access-Control-Allow-Origin'] = '*'
            return resp

