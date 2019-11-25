from django.conf.urls import url
from elastic_app import viewsets
urlpatterns = [
    url(r'^books/$', viewsets.book_search, name='books_search'),
]
