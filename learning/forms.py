from django import forms
from .models import Book
from tinymce.widgets import TinyMCE


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
