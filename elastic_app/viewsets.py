from elastic_app.documents import BookDocument
from django.shortcuts import render
from elasticsearch_dsl.query import Q
from django.utils.functional import LazyObject
from django.http import JsonResponse, Http404
from elasticsearch import TransportError
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger

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
        # print('BOOKS: ', search)
        try:
            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
        except TransportError:
            raise Http404('Index does not exist. Run `python manage.py search_index --rebuild` to create it.')

    # return render(request, 'search.html', {'books': page})
    # print(list(page))
    return JsonResponse({
        'book': {'title': 'someTitle', 'authors': 'someAuthor', 'genre': 3, 'id': 5},
        'image': 'https://hb.bizmrg.com/capsula_bucket/avatar/10.jpg'
    })


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
