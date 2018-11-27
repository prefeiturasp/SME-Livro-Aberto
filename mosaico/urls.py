from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'mosaico'
urlpatterns = [
    path('', TemplateView.as_view(template_name='mosaico/base.html'), name='home'),
]
