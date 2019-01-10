from django.urls import path

from mosaico.views import (
    DownloadView,
    ElementosListView,
    GruposListView,
    ProgramasListView,
    ProjetosAtividadesListView,
    SubelementosListView,
    SubfuncoesListView,
    SubgruposListView,
    SobreView,
    MetodologiaView,
    DeflacionamentoView,
    TutorialView,
)


app_name = 'mosaico'
urlpatterns = [
    # `Simples` visualization urls
    path('', GruposListView.as_view(), name='grupos'),
    path('grupo/<int:grupo_id>/', SubgruposListView.as_view(),
         name='subgrupos'),
    path(('grupo/<int:grupo_id>/subgrupo/<int:subgrupo_id>/'),
         ElementosListView.as_view(), name='elementos'),
    path(('grupo/<int:grupo_id>/subgrupo/<int:subgrupo_id>/'
         'elemento/<int:elemento_id>/'), SubelementosListView.as_view(),
         name='subelementos'),

    # `Tecnico` visualization urls
    path('tecnico/', SubfuncoesListView.as_view(), name='subfuncoes'),
    path('tecnico/subfuncao/<int:subfuncao_id>/', ProgramasListView.as_view(),
         name='programas'),
    path(('tecnico/subfuncao/<int:subfuncao_id>/programa/<int:programa_id>/'),
         ProjetosAtividadesListView.as_view(), name='projetos'),

    path('download/<str:section>/', DownloadView.as_view(),
         name='download'),
    path('sobre', SobreView.as_view(), name='sobre'),
    path('metodologia', MetodologiaView.as_view(), name='metodologia'),
    path('deflacionamento', DeflacionamentoView.as_view(), name='deflacionamento'),
    path('tutorial', TutorialView.as_view(), name='tutorial'),
]
