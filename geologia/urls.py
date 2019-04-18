from django.urls import path
from django.views.generic import TemplateView

from geologia.views import DownloadView, HomeView


app_name = 'geologia'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('download/<str:chart>/', DownloadView.as_view(),
         name='download'),
    path('sobre/', TemplateView.as_view(template_name='geologia/sobre.html'),
         name='sobre'),
    path('metodologia/',
         TemplateView.as_view(template_name='geologia/metodologia.html'),
         name='metodologia'),
    path('tutorial/',
         TemplateView.as_view(template_name='geologia/tutorial.html'),
         name='tutorial'),
]
