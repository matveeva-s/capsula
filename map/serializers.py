from rest_framework import serializers
from map.models import GeoPoint


class GeoPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoPoint
        fields = ('id', 'name', 'latitude', 'longitude')