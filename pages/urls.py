from django.urls import path
from .views import HomePageView, AboutPageView, TeacherListView, ManualPageView

urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about"),
    path("teachers/", TeacherListView.as_view(), name="teacher_list"),
    path("manual/", ManualPageView.as_view(), name="manual"),
    path("", HomePageView.as_view(), name="home"),
]
