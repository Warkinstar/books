from django import forms
from .models import Book, Topic, Record, SubTopic, SubRecord
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
        fields = ('title', 'access_level')


class SubTopicForm(forms.ModelForm):
    class Meta:
        model = SubTopic
        fields = ('title', 'access_level')


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('title', 'preview', 'text', 'access_level', 'image', 'document')
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'preview': TinyMCE(attrs={'cols':80, 'rows': 30}),
        }


class SubRecordForm(forms.ModelForm):
    class Meta:
        model = SubRecord
        fields = ('title', 'preview', 'text', 'access_level', 'image', 'document')
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'preview': TinyMCE(attrs={'cols':80, 'rows': 30}),
        }


