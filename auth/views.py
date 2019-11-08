from builtins import KeyError

from django.contrib.auth import logout
from django.contrib.auth.models import User as DjangoUser
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from social_django.models import UserSocialAuth

from auth.forms import UserAuthForm, DjangoUserAuthForm
from capsula.utils import complete_headers
from user.models import User
from user.serializers import UserSerializer


class LoginView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @complete_headers
    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        username = data['username']
        password = data['password']
        auth_user = get_object_or_404(DjangoUser, username=username)
        if auth_user and auth_user.check_password(password):
            request.session['member_id'] = auth_user.username
        else:
            return JsonResponse({'msg': 'Ошибка входа (проверьте логин и пароль)'}, status=401)
        token = Token.objects.get_or_create(user=auth_user)
        user = User.objects.get(django_user=auth_user)
        serializer = self.get_serializer(user)
        data = serializer.data
        return JsonResponse({**{'token': token[0].key}, **data})

    @complete_headers
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return JsonResponse({}, status=204)
        else:
            django_user = request.user
            user = User.objects.filter(django_user=django_user)
            if len(user) == 0:
                if len(User.objects.filter(email=django_user.email)) == 0:
                    oauth_user = UserSocialAuth.objects.get(user=django_user)
                    user = User.objects.create(django_user=django_user,
                                               first_name=django_user.first_name,
                                               last_name=django_user.last_name,
                                               email=django_user.email,
                                               contact=oauth_user.uid)
                else:
                    if django_user.email:
                        old_django_user = DjangoUser.objects.filter(email=django_user.email).exclude(id=django_user.id)
                        if len(old_django_user) == 1:
                            oauth_user = UserSocialAuth.objects.get(user=django_user)
                            oauth_user.user = old_django_user[0]
                            oauth_user.save()
                            django_user.delete()
                        else:
                            return JsonResponse({'detail': 'Такой email не один в системе'}, status=409)
                    else:
                        oauth_user = UserSocialAuth.objects.get(user=django_user)
                        user = User.objects.create(django_user=django_user,
                                                   first_name=django_user.first_name,
                                                   last_name=django_user.last_name,
                                                   email= oauth_user.uid + '@false.ru',
                                                   contact=oauth_user.uid)
            else:
                user = User.objects.get(django_user=django_user)
            token = Token.objects.get_or_create(user=django_user)
            serializer = self.get_serializer(user)
            data = serializer.data
            return JsonResponse({**{'token': token[0].key}, **data})


@permission_classes([IsAuthenticated])
class LogoutView(generics.RetrieveAPIView):
    queryset = DjangoUser.objects.all()

    @complete_headers
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
        return JsonResponse({})


class RegistrationView(generics.RetrieveAPIView):

    @complete_headers
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
            return JsonResponse({})
        else:
            if DjangoUser.objects.filter(username=data['username']).exists():
                return JsonResponse({'detail': 'Пользователь с таким именем уже существует'}, status=409)
            if user_form.errors['email'][0] == 'User with this Email already exists.':
                return JsonResponse({'detail': 'Адрес электронной почты уже используется'}, status=409)
            return JsonResponse({'detail': 'Ошибка создания, проверьте данные'}, status=400)
