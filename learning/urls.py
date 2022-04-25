from django.urls import path
from .views import BookListView, BookDetailView, BookNewView
from .views import SearchResultsListView
from .views import TopicListView, RecordListView, RecordDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/new/', BookNewView.as_view(), name='book_new'),

    # Страница со списком тем (и не только)
    path('', TopicListView.as_view(), name='topic_list'),
    # Список записей темы('topic')
    path('topic/<uuid:pk>/', RecordListView.as_view(), name='topic'),
    # Личная страница записи темы
    path('topic/record/<uuid:pk>/', RecordDetailView.as_view(), name='record'),

    path('search/', SearchResultsListView.as_view(), name='search_results'),
]