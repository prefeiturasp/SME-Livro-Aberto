from django.urls import path

from geologia.views import HomeView


app_name = 'geologia'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
