from django.urls import path
from .views import BookListView, BookDetailView
from .views import LearningListView, SearchResultsListView

urlpatterns = [
    path('', LearningListView.as_view(), name='learning_list'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
]