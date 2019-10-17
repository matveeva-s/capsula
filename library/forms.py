from django import forms
from library.models import Book, Swap, BookItem


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'authors', 'genre')


class BookItemForm(forms.ModelForm):
    class Meta:
        model = BookItem
        fields = ('status', 'isbn')


class SwapForm(forms.ModelForm):
    class Meta:
        model = Swap
        fields = ('id', 'status')
