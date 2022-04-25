from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, FormView
from django.views.generic import ListView, DetailView
from .models import Book, Topic, Record
from .forms import BookForm
from django.urls import reverse_lazy

'''
class LearningListView(TemplateView):
    template_name = 'learning/learning_list.html'
'''

class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'learning/book_list.html'


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'learning/book_detail.html'


class BookNewView(FormView):
    template_name = 'learning/book_new.html'
    form_class = BookForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topic_list'
    template_name = 'learning/learning_list.html'  # Список тем на странице '/learning/'


class RecordListView(DetailView):  # TopicDetailView
    model = Topic
    template_name = 'learning/record_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_list'] = self.object.record_set.all  # Получить связанную модель topic-record
        return context


class RecordDetailView(DetailView):
    model = Record
    context_object_name = 'record'
    template_name = 'learning/record_detail.html'


class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'learning/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )
