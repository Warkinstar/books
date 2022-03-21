from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from .models import Book


class LearningListView(TemplateView):
    template_name = 'learning/learning_list.html'


class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'learning/book_list.html'


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'learning/book_detail.html'
