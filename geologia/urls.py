from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'geologia'
urlpatterns = [
    path('', TemplateView.as_view(template_name='geologia/base.html'),
         name='home'),
]
