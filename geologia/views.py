from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer

from budget_execution.models import Execucao
from geologia.serializers import GeologiaSerializer, GeologiaDownloadSerializer


class HomeView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'geologia/base.html'
    queryset = Execucao.objects.filter(subgrupo__isnull=False)
    serializer_class = GeologiaSerializer

    def list(self, request):
        qs = self.get_queryset()
        subfuncao_id = self.request.GET.get('subfuncao_id', None)
        serializer = self.get_serializer(qs, subfuncao_id=subfuncao_id)
        return Response(serializer.data)

class DownloadView(generics.ListAPIView):
    renderer_classes = [CSVRenderer]
    queryset = Execucao.objects.filter(subgrupo__isnull=False)
    serializer_class = GeologiaDownloadSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        chart = self.kwargs['chart']
        serializer = self.get_serializer(qs, chart=chart)

        filename = f'geologia_{chart}'
        headers = {
            'Content-Disposition': f'attachment; filename={filename}.csv'
        }
        response = Response(serializer.data, headers=headers)
        return response
