from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^(?P<pk>\d+)/books/$', views.UserBookListView.as_view(), name='user_books_lists'),
    url(r'^(?P<pk>\d+)/books/(?P<id>\d+)/$', views.BookDetailView.as_view(), name='book_item_detail'),
]
