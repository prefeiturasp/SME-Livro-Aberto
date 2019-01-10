from django.urls import path

from geologia.views import *


app_name = 'geologia'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sobre', SobreView.as_view(), name='sobre'),
    path('metodologia', MetodologiaView.as_view(), name='metodologia'),
    path('tutorial', TutorialView.as_view(), name='tutorial'),
]
