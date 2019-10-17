from django.conf.urls import url
from library.views import books_views, swaps_views

urlpatterns = [
    url(r'^(books/)$', books_views.BookListView.as_view(), name='books_lists'),
    url(r'^(books)/(?P<id>\d+)/$', books_views.BookDetailView.as_view(), name='books_detail'),
    url(r'^(swaps/)$', swaps_views.SwapListlView.as_view(), name='swaps_lists'),
    url(r'^(swaps)/(?P<id>\d+)/$', swaps_views.SwapDetailView.as_view(), name='swaps_detail'),
    url(r'^(book_items/)$', books_views.BookItemsListView.as_view(), name='books_item_lists'),
    url(r'^(book_items)/(?P<id>\d+)/$', books_views.BookItemsDetailView.as_view(), name='books_item_detail')
]
