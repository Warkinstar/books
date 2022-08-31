from .serializers import TopicSerializer, SubTopicSerializer, RecordSerializer, SubRecordSerializer
from rest_framework import generics
from django.views.generic import TemplateView
from learning.models import Topic, SubTopic, Record, SubRecord

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

