from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.forms import BookForm
from user.serializers import UserSerializer
from library.models import BookItem, Book, Swap
from library.serializers import BookItemSerializerList, BookItemSerializerDetail, SwapSerializerDetail
from capsula.utils import upload_file


#todo шифровать пароль при регистрации и входе
@permission_classes([IsAuthenticated])
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class UserBookListView(generics.ListCreateAPIView):
    serializer_class = BookItemSerializerList
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['pk'])
        books = self.queryset.filter(owner=user)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['pk'])
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.data['title']
            authors = form.data['authors']
            existing_books = Book.objects.filter(title__contains=title, authors__contains=authors)
            if existing_books:
                book = existing_books[0]
            else:
                book = form.save()
            book_item = BookItem.objects.create(book=book, owner=user)
            book_item.save()
            return JsonResponse({})
        else:
            return JsonResponse({'msg': 'Ошибка создания, проверьте данные'}, status=400)


@permission_classes([IsAuthenticated])
class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookItemSerializerDetail
    queryset = BookItem.objects.all()

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['id']
        book = BookItem.objects.get(id=book_id)
        serializer = self.get_serializer(book)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class MeDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        token = request.headers['Authorization'][6:]
        django_user = Token.objects.get(key=token).user
        user = User.objects.get(django_user=django_user)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class UserSwapListView(generics.ListCreateAPIView):
    serializer_class = SwapSerializerDetail
    queryset = Swap.objects.all()

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['pk'])
        swaps = self.queryset.filter(reader=user)
        serializer = self.get_serializer(swaps, many=True)
        return Response(serializer.data)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def change_avatar(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_avatar = request.FILES['image']
        upload_path = 'avatar/{}'.format(pk)
        upload_file(upload_path, user_avatar)

    return JsonResponse({})


