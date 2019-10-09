from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library.models import Book, Swap
from library.serializers import BookSerializerList, SwapSerializerList


@permission_classes([IsAuthenticated])
class BookListlView(generics.RetrieveAPIView):
    serializer_class = BookSerializerList
    queryset = Book.objects.all()
      #todo придумать как возвращать не весь список а пачками по мере прогрузки
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = self.get_serializer(books, many=True)
        resp = Response(serializer.data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp


@permission_classes([IsAuthenticated])
class SwapListlView(generics.RetrieveAPIView):
    serializer_class = SwapSerializerList
    queryset = Swap.objects.all()
      #todo придумать как возвращать не весь список а пачками по мере прогрузки
    def get(self, request, *args, **kwargs):
        swaps = Swap.objects.all()
        serializer = self.get_serializer(swaps, many=True)
        resp = Response(serializer.data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp