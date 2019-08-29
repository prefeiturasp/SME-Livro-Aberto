from django.urls import path
from django.views.generic import TemplateView

from contratos.views import HomeView, download_view


app_name = 'contratos'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('download/', download_view, name='download'),
    path('sobre/', TemplateView.as_view(template_name='contratos/sobre.html'),
         name='sobre'),
]
