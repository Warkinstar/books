from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        widgets = {
            'documents': forms.ClearableFileInput(attrs={'multiple': True}),
        }