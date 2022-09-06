from django.urls import path
from .views import (
    TopicList,
    SubTopicList,
    RecordList,
    SubRecordList,
    ApiPageView,
    UserList,
)


urlpatterns = [
    path("", ApiPageView.as_view(), name="api"),
    path("topics/", TopicList.as_view(), name="topics_api"),
    path("subtopics/", SubTopicList.as_view(), name="subtopics_api"),
    path("records/", RecordList.as_view(), name="records_api"),
    path("subrecords/", SubRecordList.as_view(), name="subrecords_api"),
    path("users/", UserList.as_view(), name="users_api"),
]