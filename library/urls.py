from django.conf.urls import url
from library import views

urlpatterns = [
    url(r'^(books/)$', views.BookListlView.as_view(), name='books_lists'),
]
