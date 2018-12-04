from django.urls import path
from django.views.generic.base import TemplateView

from mosaico.views import (
    ElementosList,
    GrupoList,
    SubgruposList
)


app_name = 'mosaico'
urlpatterns = [
    path('', TemplateView.as_view(template_name='mosaico/base.html'),
         name='home'),
    path('treemap/<int:year>/', GrupoList.as_view(), name='grupos'),
    path('treemap/<int:year>/grupo/<int:grupo_id>/', SubgruposList.as_view(),
         name='subgrupos'),
    path('treemap/<int:year>/grupo/<int:grupo_id>/subgrupo/<int:subgrupo_id>/',
         ElementosList.as_view(),
         name='elementos'),
]
