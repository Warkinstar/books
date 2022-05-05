from django import forms
from .models import Book, Topic, Record
from tinymce.widgets import TinyMCE


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'preview': TinyMCE(attrs={'cols': 80, 'rows': 10}),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title',)


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('title', 'preview', 'text', 'image', 'document')
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'preview': TinyMCE(attrs={'cols':80, 'rows': 30}),
        }



