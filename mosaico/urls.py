from django.urls import path
from django.views.generic.base import TemplateView

from mosaico.views import (
    ElementosListView,
    GruposListView,
    ProgramasListView,
    SubelementosListView,
    SubfuncoesListView,
    SubgruposListView
)


app_name = 'mosaico'
urlpatterns = [
    path('', TemplateView.as_view(template_name='mosaico/base.html'),
         name='home'),

    # `Simples` visualization urls
    path('treemap/simples/<int:year>/', GruposListView.as_view(),
         name='grupos'),
    path('treemap/simples/<int:year>/grupo/<int:grupo_id>/',
         SubgruposListView.as_view(),
         name='subgrupos'),
    path(('treemap/simples/<int:year>/grupo/<int:grupo_id>/'
          'subgrupo/<int:subgrupo_id>/'),
         ElementosListView.as_view(),
         name='elementos'),
    path(('treemap/simples/<int:year>/grupo/<int:grupo_id>/'
          'subgrupo/<int:subgrupo_id>/elemento/<int:elemento_id>/'),
         SubelementosListView.as_view(),
         name='subelementos'),

    # `Tecnico` visualization urls
    path('treemap/tecnico/<int:year>/', SubfuncoesListView.as_view(),
         name='subfuncoes'),
    path('treemap/tecnico/<int:year>/subfuncao/<int:subfuncao_id>/',
         ProgramasListView.as_view(),
         name='programas'),
]
