from django.urls import path
from django.views.generic import TemplateView

from contratos.views import HomeView, download_view


app_name = 'contratos'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('download/', download_view, name='download'),
    path('sobre/', TemplateView.as_view(template_name='contratos/sobre.html'),
         name='sobre'),
    path('saiba-mais/', TemplateView.as_view(template_name='contratos/saiba_mais.html'), name='saiba_mais'),
    path('metodologia', TemplateView.as_view(template_name='contratos/metodologia.html'), name='metodologia'),
    path('tutorial/', TemplateView.as_view(template_name='contratos/tutorial.html'), name='tutorial'),

]
