from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

group = 'teachers'

class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class TeacherListView(TemplateView):
    template_name = 'teacher_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = get_user_model()
        context['teacher_list'] = obj.objects.filter(groups__name=group)
        return context

