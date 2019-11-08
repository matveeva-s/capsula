from django.shortcuts import get_object_or_404
from django.core.serializers import json
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.permissions import IsAuthenticated

from capsula.settings.common import MEDIA_URL
from capsula.utils import upload_file, get_user_from_request, complete_headers
from user.forms import UserForm
from user.models import User
from user.serializers import UserSerializer

#todo шифровать пароль при регистрации и входе
# https://habr.com/ru/post/120380/ статья по безопасной передаче логина-пароля с фронта на бэк
@permission_classes([IsAuthenticated])
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = get_object_or_404(User, id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class MeDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        serializer = self.get_serializer(user)
        data = serializer.data
        return Response(data)

    @complete_headers
    def put(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        user = get_user_from_request(request)
        form = UserForm(data)
        # print(request.data)
        if form.is_valid():
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.location = data.get('location')
            user.contact = data.get('vk')
            if request.data.get('image'):
                user_avatar = request.data.get('image')
                upload_path = 'avatar/{}.jpg'.format(user.id)
                upload_file(upload_path, user_avatar)
                user.avatar = MEDIA_URL + upload_path
            user.save()
            serializer = self.get_serializer(user)
            data = serializer.data
            return Response(data)
        else:
            return JsonResponse({'detail': 'Ошибка создания, проверьте данные'}, status=400)

@permission_classes([IsAuthenticated])
class UserListView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

