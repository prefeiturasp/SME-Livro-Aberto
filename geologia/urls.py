from django.urls import path

from geologia.views import DownloadView, HomeView


app_name = 'geologia'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('download/<str:chart>/', DownloadView.as_view(),
         name='download'),
]
