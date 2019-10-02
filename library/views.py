from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library.models import Book
from library.serializers import BookSerializerList


@permission_classes([IsAuthenticated])
class BookListlView(generics.RetrieveAPIView):
    serializer_class = BookSerializerList
    queryset = Book.objects.all()
      #todo придумать как возвращать не весь список а пачками по мере прогрузки
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
