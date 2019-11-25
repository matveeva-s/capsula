from django.conf.urls import url

from management import views
urlpatterns = [
    url(r'^(complaint_book/)$', views.ComplaintBookListView.as_view(), name='complaint_book_lists'),
    url(r'^(complaint_book)/(?P<id>\d+)/$', views.ComplaintBookDetailView.as_view(), name='complaint_book_detail'),

    url(r'^(complaint_user/)$', views.ComplaintUserListView.as_view(), name='complaint_user_list'),
    url(r'^(complaint_user)/(?P<id>\d+)/$', views.ComplaintUserDetailView.as_view(), name='complaint_user_detail'),
]