from django import forms
from library.models import Book, Swap, BookItem


class BookForm(forms.ModelForm):
    title = forms.CharField()
    authors = forms.CharField()
    genre = forms.IntegerField()

    class Meta:
        model = Book
        fields = ('title', 'authors', 'genre')


class BookItemForm(forms.ModelForm):
    class Meta:
        model = BookItem
        fields = ('status', 'isbn')


