from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'learning/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )
