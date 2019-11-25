from django.conf.urls import url
from map import views

urlpatterns = [
    url(r'^$', views.GeoPointsListView.as_view(), name='geo_point_list'),
    url(r'^(?P<id>\d+)/$', views.GeoPointDetailView.as_view(), name='geo_point_detail')
]