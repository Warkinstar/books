from rest_framework import serializers
from learning.models import Topic, SubTopic, Record, SubRecord
from django.contrib.auth import get_user_model


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = "__all__"


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = "__all__"


class SubRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRecord
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("last_name", "first_name", "middle_name", "email", "groups",)


