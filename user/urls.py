from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='user_list'),
    url(r'^(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^(me)/$', views.MeDetailView.as_view(), name='my_profile')
]
