from django.urls import path
from .views import HomePageView, AboutPageView, TeacherListView

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('', HomePageView.as_view(), name='home'),
]
