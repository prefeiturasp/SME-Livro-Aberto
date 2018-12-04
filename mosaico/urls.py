from django.urls import path
from django.views.generic.base import TemplateView

from mosaico.views import (
    ElementosList,
    GruposList,
    SubelementosList,
    SubfuncoesList,
    SubgruposList
)


app_name = 'mosaico'
urlpatterns = [
    path('', TemplateView.as_view(template_name='mosaico/base.html'),
         name='home'),

    path('treemap/simples/<int:year>/', GruposList.as_view(), name='grupos'),
    path('treemap/simples/<int:year>/grupo/<int:grupo_id>/',
         SubgruposList.as_view(),
         name='subgrupos'),
    path(('treemap/simples/<int:year>/grupo/<int:grupo_id>/'
          'subgrupo/<int:subgrupo_id>/'),
         ElementosList.as_view(),
         name='elementos'),
    path(('treemap/simples/<int:year>/grupo/<int:grupo_id>/'
          'subgrupo/<int:subgrupo_id>/elemento/<int:elemento_id>/'),
         SubelementosList.as_view(),
         name='subelementos'),

    path('treemap/tecnico/<int:year>/', SubfuncoesList.as_view(),
         name='subfuncoes'),
]
