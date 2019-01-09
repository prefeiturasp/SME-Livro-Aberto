from django.urls import path

from geologia.views import *


app_name = 'geologia'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sobre', SobreView.as_view(), name='sobre'),
]
