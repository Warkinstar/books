from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, FormView
from django.views.generic import ListView, DetailView
from .models import Book, Topic, Record
from .forms import BookForm, TopicForm, RecordForm
from django.urls import reverse_lazy
from django.urls import reverse


class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'learning/book_list.html'


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'learning/book_detail.html'


class BookNewView(LoginRequiredMixin, FormView):
    template_name = 'learning/book_new.html'
    form_class = BookForm
    success_url = reverse_lazy('book_list')
    login_url = 'account_login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TopicListView(ListView):
    """Список тем"""
    model = Topic
    context_object_name = 'topic_list'
    template_name = 'learning/learning_list.html'  # Список тем на странице '/learning/'


class TopicNewView(LoginRequiredMixin, FormView):
    """Создание новой темы"""
    template_name = 'learning/topic_new.html'
    form_class = TopicForm
    success_url = reverse_lazy('topic_list')
    login_url = 'account_login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RecordListView(DetailView):  # TopicDetailView
    """Список записей темы"""
    model = Topic
    context_object_name = 'topic'
    template_name = 'learning/record_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_list'] = self.object.record_set.all  # Получить связанную модель topic-record
        return context


class RecordDetailView(DetailView):
    """Личная страничка записи"""
    model = Record
    context_object_name = 'record'
    template_name = 'learning/record_detail.html'


class RecordNewView(LoginRequiredMixin, FormView):
    """Создать новую запись (связанную с темой)"""
    template_name = 'learning/record_new.html'
    form_class = RecordForm
    login_url = 'account_login'

    def form_valid(self, form):
        """Привязка к теме и привязка к автору"""
        obj = form.save(commit=False)
        obj.topic_id = self.kwargs['pk']
        obj.author = self.request.user
        obj.save()
        return super(RecordNewView, self).form_valid(form)

    def get_success_url(self):
        """Переход на список записей темы"""
        return reverse('topic', kwargs={'pk': self.kwargs['pk']})

''' Переход на созданную страницу (не работает)
    def get_success_url(self):
        return reverse('record', kwargs={'pk': self.obj.pk})
'''


class SearchResultsListView(ListView):
    """Поиск по книгам (пока что)"""
    model = Book
    context_object_name = 'book_list'
    template_name = 'learning/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )
