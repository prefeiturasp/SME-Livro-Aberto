from django.urls import path
from django.views.generic import TemplateView

from regionalizacao.views import HomeView


app_name = 'regionalizacao'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('saiba-mais/',
        TemplateView.as_view(template_name='regionalizacao/saiba_mais.html'),
        name='saiba_mais'),
]
