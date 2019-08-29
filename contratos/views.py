import os

from datetime import date

from django.http import HttpResponse, Http404
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from contratos.constants import GENERATED_XLSX_PATH
from contratos.models import ExecucaoContrato
from contratos.serializers import ExecucaoContratoSerializer


class ExecucaoContratoFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name='year', lookup_expr='year')

    class Meta:
        model = ExecucaoContrato
        fields = ['year']


class HomeView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ExecucaoContratoFilter
    # TODO: add view tests
    queryset = ExecucaoContrato.objects.filter(categoria__isnull=False)
    serializer_class = ExecucaoContratoSerializer
    template_name = 'contratos/home.html'

    def filter_queryset(self, queryset):
        if 'year' not in self.request.query_params:
            curr_year = date.today().year
            queryset = queryset.filter(year__year=curr_year)
        return super().filter_queryset(queryset)

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['categoria_id'] = self.request.query_params.get(
            'categoria_id', None)
        kwargs['year'] = self.request.query_params.get('year', None)
        return serializer_class(*args, **kwargs)


# TODO: add download view tests
def download_view(request):
    if 'year' in request.GET:
        year = request.GET['year']
    else:
        year = date.today().year

    filename = f'contratos_{year}.xlsx'
    filepath = os.path.join(GENERATED_XLSX_PATH, filename)
    if not os.path.exists(filepath):
        raise Http404

    with open(filepath, 'rb') as fh:
        response = HttpResponse(
            fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = (
            'inline; filename=' + os.path.basename(filepath))
        return response
