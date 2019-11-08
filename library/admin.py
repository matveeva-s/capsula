from django.contrib import admin
from .models import Book, BookItem, Swap, Wishlist

admin.site.register(Book)
admin.site.register(BookItem)
admin.site.register(Swap)
admin.site.register(Wishlist)
