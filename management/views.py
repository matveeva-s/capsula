from django.core.serializers import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from capsula.utils import complete_headers, get_user_from_request
from library.models import Book
from management.forms import ComplaintBookForm, ComplaintUserForm
from management.models import ComplaintBook, ComplaintUser
from user.models import User, UserSubscription


@permission_classes([IsAuthenticated])
class ComplaintBookListView(generics.RetrieveAPIView):
    queryset = ComplaintBook.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        #pass
        users = User.objects.all()
        for user in users:
            if len(UserSubscription.objects.filter(user=user)) == 0:
                UserSubscription.objects.create(user=user)
        return JsonResponse({})

    @complete_headers
    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        author = get_user_from_request(request)
        form = ComplaintBookForm(data)
        if form.is_valid():
            content = data.get('content')
            book = get_object_or_404(Book, id=data.get('book'))
            comment = data.get('comment')
            ComplaintBook.objects.create(author=author,
                                         status=ComplaintBook.NEW,
                                         content=content,
                                         book=book,
                                         comment=comment)
            return JsonResponse({})
        else:
            return JsonResponse({'detail': 'Ошибка создания, проверьте данные'}, status=400)


@permission_classes([IsAuthenticated])
class ComplaintBookDetailView(generics.RetrieveAPIView):
    queryset = ComplaintBook.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        pass


@permission_classes([IsAuthenticated])
class ComplaintUserListView(generics.RetrieveAPIView):
    queryset = ComplaintUser.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        pass

    @complete_headers
    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        author = get_user_from_request(request)
        form = ComplaintUserForm(data)
        if form.is_valid():
            content = data.get('content')
            user = get_object_or_404(User, id=data.get('user'))
            comment = data.get('comment')
            ComplaintUser.objects.create(author=author,
                                                     status=ComplaintBook.NEW,
                                                     content=content,
                                                     user=user,
                                                     comment=comment)
            return JsonResponse({})
        else:
            return JsonResponse({'detail': 'Ошибка создания, проверьте данные'}, status=400)


@permission_classes([IsAuthenticated])
class ComplaintUserDetailView(generics.RetrieveAPIView):
    queryset = ComplaintUser.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        pass
