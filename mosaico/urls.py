from django.urls import path
from django.views.generic.base import TemplateView

from mosaico.views import (
    GrupoList,
)


app_name = 'mosaico'
urlpatterns = [
    path('', TemplateView.as_view(template_name='mosaico/base.html'),
         name='home'),
    path('treemap/<int:year>/', GrupoList.as_view(), name='grupos'),
]
