from django.utils.functional import LazyObject
from elasticsearch_dsl.query import Q
from elastic_app.documents import BookDocument
from library.models import Book


def book_search(q=None, genre=None):
    search = BookDocument.search()
    search_results = Book.objects.all()
    if q:
        search = search.filter(
            Q('prefix', title=q) | Q('prefix', authors=q)
        )
        search_results = SearchResults(search)
    if genre:
        search = search.query('match', genre=genre)
        search_results = SearchResults(search)
    return search_results


class SearchResults(LazyObject):

    def __init__(self, search_object):
        self._wrapped = search_object

    def __len__(self):
        return self._wrapped.count()

    def __getitem__(self, index):
        search_results = self._wrapped[index]
        if isinstance(index, slice):
            search_results = list(search_results)
        return search_results
