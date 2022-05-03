from django import forms
from .models import Book, Topic, Record
from tinymce.widgets import TinyMCE


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title',)


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('title', 'text', 'image', 'document', 'author')
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }



