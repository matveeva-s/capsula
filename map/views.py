from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json

from capsula.utils import complete_headers, get_user_from_request
from map.models import GeoPoint
from map.serializers import GeoPointsSerializer


@permission_classes([IsAuthenticated])
class GeoPointsListView(generics.RetrieveAPIView):
    serializer_class = GeoPointsSerializer
    queryset = GeoPoint.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        points = GeoPoint.objects.filter(user=user)
        if len(points) == 0:
            data = []
            return Response(data)
        else:
            serializer = self.get_serializer(points, many=True)
            data = serializer.data
            return Response(data)

    @complete_headers
    def post(self, request, *args, **kwargs):
        if request.content_type == 'text/plain;charset=UTF-8':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        user = get_user_from_request(request)
        name = data['name']
        latitude = data['latitude']
        longitude = data['longitude']
        point = GeoPoint.objects.create(name=name, latitude=latitude, longitude=longitude, user=user)
        serializer = self.get_serializer(point)
        data = serializer.data
        return Response(data)


@permission_classes([IsAuthenticated])
class GeoPointDetailView(generics.RetrieveAPIView):
    serializer_class = GeoPointsSerializer
    queryset = GeoPoint.objects.all()

    @complete_headers
    def get(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        point_id = self.kwargs['id']
        point = get_object_or_404(GeoPoint, pk=point_id)
        serializer = self.get_serializer(point)
        data = serializer.data
        return Response(data)

    @complete_headers
    def put(self):
        pass

    @complete_headers
    def delete(self, request, *args, **kwargs):
        user = get_user_from_request(request)
        point_id = self.kwargs['id']
        point = get_object_or_404(GeoPoint, pk=point_id)
        if point.user != user:
            return JsonResponse({'detail': 'Пользователь может удалять только свои точки'}, status=403)
        else:
            point.delete()
            return JsonResponse({})
