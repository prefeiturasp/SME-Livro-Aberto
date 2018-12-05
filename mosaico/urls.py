from django.urls import path
from django.views.generic.base import TemplateView

from mosaico.views import (
    ElementosListView,
    GruposListView,
    ProgramasListView,
    ProjetosAtividadesListView,
    SubelementosListView,
    SubfuncoesListView,
    SubgruposListView
)


app_name = 'mosaico'
urlpatterns = [
    path('', TemplateView.as_view(template_name='mosaico/base.html'),
         name='home'),

    # `Simples` visualization urls
    path('simples/<int:year>/', GruposListView.as_view(),
         name='grupos'),
    path('simples/<int:year>/grupo/<int:grupo_id>/',
         SubgruposListView.as_view(),
         name='subgrupos'),
    path(('simples/<int:year>/grupo/<int:grupo_id>/'
          'subgrupo/<int:subgrupo_id>/'),
         ElementosListView.as_view(),
         name='elementos'),
    path(('simples/<int:year>/grupo/<int:grupo_id>/'
          'subgrupo/<int:subgrupo_id>/elemento/<int:elemento_id>/'),
         SubelementosListView.as_view(),
         name='subelementos'),

    # `Tecnico` visualization urls
    path('tecnico/<int:year>/', SubfuncoesListView.as_view(),
         name='subfuncoes'),
    path('tecnico/<int:year>/subfuncao/<int:subfuncao_id>/',
         ProgramasListView.as_view(),
         name='programas'),
    path(('tecnico/<int:year>/subfuncao/<int:subfuncao_id>/'
          'programa/<int:programa_id>/'),
         ProjetosAtividadesListView.as_view(),
         name='projetos'),
]
