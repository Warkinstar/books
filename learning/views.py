from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, FormView
from django.views.generic import ListView, DetailView, CreateView
from .models import Book
from .forms import BookForm
from django.urls import reverse_lazy

#from django.views.generic.edit import FormView


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


class BookNewView(FormView):
    template_name = 'learning/book_new.html'
    form_class = BookForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
'''
    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                file_instance = form_class(document=f)
                file_instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
'''



class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'learning/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )
