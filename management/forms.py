from django import forms

from management.models import ComplaintBook, ComplaintUser


class ComplaintBookForm(forms.ModelForm):
    class Meta:
        model = ComplaintBook
        fields = ('content', 'book', 'comment')


class ComplaintUserForm(forms.ModelForm):
    class Meta:
        model = ComplaintUser
        fields = ('content', 'user', 'comment')