from .serializers import (
    TopicSerializer,
    SubTopicSerializer,
    RecordSerializer,
    SubRecordSerializer,
    UserSerializer,
)
from rest_framework import generics, permissions
from django.views.generic import TemplateView
from learning.models import Topic, SubTopic, Record, SubRecord
from django.contrib.auth import get_user_model

"""
generics.ListCreateAPIView  # Список и Создание
generics.RetrieveUpdateDestroyAPIView  # Detail и UpdateDestroy
"""


class ApiPageView(TemplateView):
    template_name = "api.html"

class TopicList(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class SubTopicList(generics.ListAPIView):
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicSerializer


class RecordList(generics.ListAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class SubRecordList(generics.ListAPIView):
    queryset = SubRecord.objects.all()
    serializer_class = SubRecordSerializer


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

