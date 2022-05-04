from django.urls import path
from .views import BookListView, BookDetailView, BookNewView
from .views import SearchResultsListView
from .views import TopicListView, RecordListView, RecordDetailView
from .views import TopicNewView, RecordNewView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/new/', BookNewView.as_view(), name='book_new'),

    path('', TopicListView.as_view(), name='topic_list'),  # Страница со списком тем (и не только(books))
    path('topic-<uuid:pk>/', RecordListView.as_view(), name='topic'),  # Список записей темы('topic')
    path('topic-new/', TopicNewView.as_view(), name='topic_new'),  # Новая тема

    path('topic/record-<uuid:pk>/', RecordDetailView.as_view(), name='record'),  # Личная страница записи опред-й темы
    path('topic/<uuid:pk>/record-new/', RecordNewView.as_view(), name='record_new'),  # Новая запись опред-й темы (pk)

    path('search/', SearchResultsListView.as_view(), name='search_results'),  # Поиск по книгам (пока что)
]