from django.urls import path
from .views import SignupPageView

urlpatterns = [
    # Можно удалить
    path('signup/', SignupPageView.as_view(), name='signup'),
]