from django.urls import path

from geologia.views import GeologiaView


app_name = 'geologia'
urlpatterns = [
    path('', GeologiaView.as_view(), name='home'),
]
