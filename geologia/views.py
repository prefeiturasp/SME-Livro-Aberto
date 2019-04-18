from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer

from budget_execution.constants import SME_ORGAO_ID
from budget_execution.models import Execucao
from geologia.serializers import GeologiaSerializer, GeologiaDownloadSerializer


class HomeView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'geologia/base.html'
    queryset = Execucao.objects.filter(is_minimo_legal=False,
                                       orgao__id=SME_ORGAO_ID)
    serializer_class = GeologiaSerializer

    def list(self, request):
        qs = self.get_queryset()
        subfuncao_id = self.request.GET.get('subfuncao_id', None)
        serializer = self.get_serializer(qs, subfuncao_id=subfuncao_id)
        return Response(serializer.data)


class DownloadView(generics.ListAPIView):
    renderer_classes = [XLSXRenderer, CSVRenderer]
    queryset = Execucao.objects.filter(is_minimo_legal=False,
                                       orgao__id=SME_ORGAO_ID)
    serializer_class = GeologiaDownloadSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        chart = self.kwargs['chart']

        subfuncao_id = self.request.GET.get('subfuncao_id', None)
        serializer = self.get_serializer(qs, chart=chart,
                                         subfuncao_id=subfuncao_id)

        filename = f'geologia_{chart}'
        if subfuncao_id:
            filename += '_filtrado'
        file_extension = request.accepted_renderer.format
        filename += f'.{file_extension}'

        headers = {
            'Content-Disposition': f'attachment; filename={filename}'
        }
        response = Response(serializer.data, headers=headers)
        return response
