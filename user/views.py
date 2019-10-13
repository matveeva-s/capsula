from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from user.models import User
from library.models import BookItem, Swap
from user.serializers import UserSerializer
from library.serializers import BookItemSerializerList, BookItemSerializerDetail, SwapSerializerList
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
class UserBookListView(generics.ListCreateAPIView):
    serializer_class = BookItemSerializerList
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['pk'])
        books = self.queryset.filter(owner=user)
        serializer = self.get_serializer(books, many=True)
        resp = Response(serializer.data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


@permission_classes([IsAuthenticated])
class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookItemSerializerDetail
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['id']
        book = BookItem.objects.get(id=book_id)
        serializer = self.get_serializer(book)
        resp =  Response(serializer.data)
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


@permission_classes([IsAuthenticated])
class UserSwapListView(generics.ListCreateAPIView):
    serializer_class = SwapSerializerList
    queryset = Swap.objects.all()

    def get(self, request, *args, **kwargs):
        pass

@permission_classes([IsAuthenticated])
class UserSwapDetailView(generics.ListCreateAPIView):
    pass