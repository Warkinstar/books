from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from .models import Book


class LearningListView(TemplateView):
    template_name = 'learning/learning_list.html'


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'learning/book_list.html'
    login_url = 'account_login'


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'learning/book_detail.html'
    login_url = 'account_login'
    permission_required = 'learning.special_status'