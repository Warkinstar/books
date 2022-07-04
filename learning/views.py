from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, FormView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Book, Topic, Record, SubTopic, SubRecord
from .forms import BookForm, TopicForm, RecordForm, SubTopicForm, SubRecordForm
from django.urls import reverse_lazy
from django.urls import reverse

group = 'teachers'  # Используется для проверки состояния пользователя в группе


def available_context(user, object):
    """
    Принимает экземпляр текущего пользователя(self.request.user) и объект (Topic).
    Возвращает список экземпляров соответствующий уровню доступа пользователя.
    """
    if user.is_authenticated:
        if user.groups.filter(name=group).exists():
            content = object.objects.filter(Q(access_level=0) | Q(access_level=1) | Q(author=user))
        else:
            content = object.objects.filter(Q(access_level=0) | Q(author=user))
        if user.is_superuser:
            content = object.objects.all()
    else:
        content = object.objects.filter(Q(access_level=0))

    return content

def available_context_set(user, object_set):
    """Принимает экземпляр текущего пользователя(self.request.user) и связанный объект(topic.record_set)
       Возвращает список экземпляров соответствующий доступу пользователя.
    """
    if user.is_authenticated:
        if user.groups.filter(name=group).exists():
            content = object_set.filter(Q(access_level=0) | Q(access_level=1) | Q(author=user))
        else:
            content = object_set.filter(Q(access_level=0) | Q(author=user))
        if user.is_superuser:
            content = object_set.all()
    else:
        content = object_set.filter(Q(access_level=0))

    return content


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
    template_name = 'learning/topic_list.html'  # Список тем на странице '/learning/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        obj = Topic  # self.object_list
        context['topic_list'] = available_context(user, obj)
        return context


class TopicNewView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """Создание новой темы"""
    template_name = 'learning/topic_new.html'
    form_class = TopicForm
    success_url = reverse_lazy('topic_list')
    login_url = 'account_login'

    def test_func(self):
        return self.request.user.groups.filter(name=group).exists()  # Объект еще пока не существует

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)


class RecordListView(UserPassesTestMixin, DetailView):  # TopicDetailView
    """Список записей и подТем темы"""
    model = Topic
    context_object_name = 'topic'
    template_name = 'learning/record_list.html'

    def test_func(self):
        obj = self.get_object()
        if obj.access_level == 1:
            return self.request.user.groups.filter(name=group).exists() or obj.author == self.request.user
        elif obj.access_level == 2:
            return obj.author == self.request.user or self.request.user.is_superuser
        else:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        obj = self.object  # can so self.get_object() (only DetailView)
        context['record_list'] = available_context_set(user, obj.record_set)
        context['subtopic_list'] = available_context_set(user, obj.subtopic_set)
        return context


class RecordDetailView(UserPassesTestMixin, DetailView):
    """Личная страничка записи"""
    model = Record
    context_object_name = 'record'
    template_name = 'learning/record_detail.html'

    def test_func(self):
        obj = self.get_object()
        if obj.access_level == 1:
            return self.request.user.groups.filter(name=group).exists() or self.request.user.is_superuser
        elif obj.access_level == 2:
            return obj.author == self.request.user or self.request.user.is_superuser
        else:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        obj = self.object  # self.get_object()
        obj_meta = obj._meta.model  # Все записи Темы из текущего экземпляра
        #context['record_list'] = available_context(user, obj._meta.model)
        context['record_list'] = available_context(user, obj_meta)
        context['topic_list'] = available_context(user, Topic)
        return context


class RecordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # Если access_level = 2?
    model = Record
    fields = ('title', 'preview', 'text', 'access_level', 'image', 'document')
    template_name = 'learning/record_update.html'
    login_url = 'account_login'

    def test_func(self):
        """Если вернет True откроет доступ"""
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.groups.filter(name=group).exists()


class RecordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # Если access_level = 2?
    """Удаляет определенную запись"""
    model = Record
    template_name = 'learning/record_delete.html'
    login_url = 'account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.groups.filter(name=group).exists()

    def get_success_url(self):
        """Переход на тему удаленной записи"""
        return reverse('topic', kwargs={'pk': self.object.topic_id})


class RecordNewView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """Создать новую запись (связанную с темой)"""
    template_name = 'learning/record_new.html'
    form_class = RecordForm
    login_url = 'account_login'

    def test_func(self):
        return self.request.user.groups.filter(name=group).exists()

    def form_valid(self, form):
        """Привязка к теме и привязка к автору"""
        obj = form.save(commit=False)
        obj.topic_id = self.kwargs['pk']
        obj.author = self.request.user
        obj.save()
        return super(RecordNewView, self).form_valid(form)

    def get_success_url(self):
        """Переход на список записей и подзаписей темы"""
        return reverse('topic', kwargs={'pk': self.kwargs['pk']})


''' Переход на созданную страницу (не работает)
    def get_success_url(self):
        return reverse('record', kwargs={'pk': self.obj.pk})
'''


class SubTopicNewView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'learning/subtopic_new.html'
    form_class = SubTopicForm
    login_url = 'account_login'

    # success_url = reverse_lazy('topic_list')

    def test_func(self):
        return self.request.user.groups.filter(name=group).exists()

    def form_valid(self, form):
        """Привязка подТемы к Теме"""
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.topic_id = self.kwargs['pk']
        obj.save()
        return super(SubTopicNewView, self).form_valid(form)

    def get_success_url(self):
        """Переход на список записей и подТем темы"""
        return reverse('topic', kwargs={'pk': self.kwargs['pk']})


class SubRecordListView(UserPassesTestMixin, DetailView):
    """Список записей подТемы"""
    model = SubTopic
    context_object_name = 'subtopic'
    template_name = 'learning/subrecord_list.html'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if obj.access_level == 1:
            return user.groups.filter(name=group).exists() or user.is_superuser
        elif obj.access_level == 2:
            return obj.author == user or user.is_superuser
        else:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        obj = self.object
        obj_meta = obj._meta.model
        context['subtopic_list'] = available_context(user, obj_meta)
        context['subrecord_list'] = available_context_set(user, obj.subrecord_set)
        return context


class SubRecordDetailView(UserPassesTestMixin, DetailView):
    model = SubRecord
    context_object_name = 'subrecord'
    template_name = 'learning/subrecord_detail.html'

    def test_func(self):
        obj = self.get_object()
        if obj.access_level == 1:
            return self.request.user.groups.filter(name=group).exists() or self.request.user.is_superuser
        elif obj.access_level == 2:
            return obj.author == self.request.user or self.request.user.is_superuser
        else:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        obj = self.object
        obj_meta = obj._meta.model
        context['subrecord_list'] = available_context(user, obj_meta)
        return context


class SubRecordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubRecord
    fields = ('title', 'preview', 'text', 'access_level', 'image', 'document')
    template_name = 'learning/subrecord_update.html'
    login_url = 'account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.groups.filter(name=group).exists()


class SubRecordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubRecord
    success_url = reverse_lazy('topic_list')
    template_name = 'learning/subrecord_delete.html'
    login_url = 'account_login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.groups.filter(name=group).exists()

    def get_success_url(self):
        """Переход на подТему удаленной записи"""
        return reverse('subtopic', kwargs={'pk': self.object.subtopic_id})


class SubRecordNewView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """Создать новую запись(подзапись) подТемы"""
    template_name = 'learning/subrecord_new.html'
    form_class = SubRecordForm
    login_url = 'account_login'

    # success_url = reverse_lazy('topic_list')

    def test_func(self):
        return self.request.user.groups.filter(name=group).exists()

    def form_valid(self, form):
        """Привязка записи к подтеме и к автору"""
        obj = form.save(commit=False)
        obj.subtopic_id = self.kwargs['pk']
        obj.author = self.request.user
        obj.save()
        return super(SubRecordNewView, self).form_valid(form)

    def get_success_url(self):
        return reverse('subtopic', kwargs={'pk': self.kwargs['pk']})


class SearchResultsListView(ListView):  # Полнотекстный поиск нужен ли?
    """Поиск по Темам, Записям, ПодТемам, ПодЗаписям"""
    model = Topic
    template_name = 'learning/search_results.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)
        context['topic_list'] = Topic.objects.filter(Q(title__icontains=query))
        context['record_list'] = Record.objects.filter(
            Q(title__icontains=query) | Q(preview__icontains=query) | Q(text__icontains=query))
        context['subtopic_list'] = SubTopic.objects.filter(Q(title__icontains=query))
        context['subrecord_list'] = SubRecord.objects.filter(
            Q(title__icontains=query) | Q(preview__icontains=query) | Q(text__icontains=query))
        return context
