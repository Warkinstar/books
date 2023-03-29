from django.urls import path
from .views import BookListView, BookDetailView, BookNewView
from .views import SearchResultsListView
from .views import TopicListView, RecordListView, RecordDetailView
from .views import TopicNewView, RecordNewView, RecordUpdateView, RecordDeleteView
from .views import SubRecordListView, SubRecordDetailView, SubRecordUpdateView, SubRecordDeleteView
from .views import SubTopicNewView, SubRecordNewView
from .views import RecordFileCreateView


urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/new/', BookNewView.as_view(), name='book_new'),

    # Topic-Record
    path('', TopicListView.as_view(), name='topic_list'),  # Страница со списком тем (и не только(books))
    path('topic-<uuid:pk>/', RecordListView.as_view(), name='topic'),  # Список записей темы('topic')
    path('topic-new/', TopicNewView.as_view(), name='topic_new'),  # Новая тема
    path('topic/record-<uuid:pk>/', RecordDetailView.as_view(), name='record'),  # Личная страница записи опред-й темы
    path('topic/record-<uuid:pk>/files', RecordFileCreateView.as_view(), name='record_files'),  # Файлы записи
    path('topic/record-<uuid:pk>/update', RecordUpdateView.as_view(), name='record_update'),  # Страница редактирования записи
    path('topic/record-<uuid:pk>/delete', RecordDeleteView.as_view(), name='record_delete'),  # Страница удаление записи
    path('topic/<uuid:pk>/record-new/', RecordNewView.as_view(), name='record_new'),  # Новая запись опред-й темы (pk)

    # SubTopic-SubRecord
    path('topic/subtopic-<uuid:pk>/', SubRecordListView.as_view(), name = 'subtopic'),  # Список подзаписей (записей подТемы)
    path('topic/<uuid:pk>/subtopic-new/', SubTopicNewView.as_view(), name='subtopic_new'),  # Новая подТема опред-й темы (pk)
    path('topic/subtopic/subrecord-<uuid:pk>/', SubRecordDetailView.as_view(), name='subrecord'),  #  Личная страница записи подТемы
    # path('topic/subtopic/subrecord-<uuid:pk>/files/', SubRecordDetailView.as_view(), name='subrecord_files'),  # Файлы подЗаписи
    path('topic/subtopic/subrecord-<uuid:pk>/update', SubRecordUpdateView.as_view(), name='subrecord_update'), # Страница редактирования подзаписи
    path('topic/subtopic/subrecord-<uuid:pk>/delete', SubRecordDeleteView.as_view(), name='subrecord_delete'), # Страница удаления подзаписи
    path('topic/subtopic-<uuid:pk>/subrecord-new/', SubRecordNewView.as_view(), name='subrecord_new'),  # Добавление записи подТемы

    path('search/', SearchResultsListView.as_view(), name='search_results'),  # Поиск по книгам (пока что)
]