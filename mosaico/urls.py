from django.urls import path

from mosaico.views import (
    DownloadView,
    HomeView,
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
    path('', HomeView.as_view(),
         name='home'),

    # `Simples` visualization urls
    path('<int:year>/', GruposListView.as_view(),
         name='grupos'),
    path('<int:year>/grupo/<int:grupo_id>/',
         SubgruposListView.as_view(),
         name='subgrupos'),
    path(('<int:year>/grupo/<int:grupo_id>/'
          'subgrupo/<int:subgrupo_id>/'),
         ElementosListView.as_view(),
         name='elementos'),
    path(('<int:year>/grupo/<int:grupo_id>/'
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

    path('download/', DownloadView.as_view(),
         name='download'),
]
