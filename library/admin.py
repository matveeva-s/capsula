from django.contrib import admin
from .models import Book, BookItem, Swap

admin.site.register(Book)
admin.site.register(BookItem)
admin.site.register(Swap)
