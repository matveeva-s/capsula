from django.contrib import admin
from .models import Book, BookItem, Swap, Wishlist


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'authors', 'genre', 'image')


admin.site.register(Book, BookAdmin)
admin.site.register(BookItem)
admin.site.register(Swap)
admin.site.register(Wishlist)
