from elastic_app.documents import BookDocument
from rest_framework.response import Response
from elasticsearch_dsl.query import Q
from django.utils.functional import LazyObject
from django.http import Http404, JsonResponse
from elasticsearch import TransportError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import book_search_serializer
from rest_framework.decorators import api_view


@api_view(('GET',))
def book_search(request):
    q = request.GET.get('q')
    paginate_by = 3
    search = BookDocument.search()

    if q:
        search = search.filter(
            Q('prefix', title=q) | Q('prefix', authors=q)
        )
        search_results = SearchResults(search)
        paginator = Paginator(search_results, paginate_by)
        page_number = request.GET.get("page")
        try:
            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
        except TransportError:
            raise Http404('Index does not exist. Run `python manage.py search_index --rebuild` to create it.')
        data = book_search_serializer(page)
        return Response(data)
    return JsonResponse({'detail': 'Something is wrong in search'}, status=404)


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
