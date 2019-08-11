from datetime import date

from django_filters import rest_framework as filters
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from contratos.models import EmpenhoSOFCache, ExecucaoContrato
from contratos.serializers import (
    EmpenhoSOFCacheSerializer, ExecucaoContratoSerializer)


class ExecucaoContratoFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name='year', lookup_expr='year')

    class Meta:
        model = ExecucaoContrato
        fields = ['year']


class HomeView(generics.ListAPIView):
    # TODO: add tests
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ExecucaoContratoFilter
    queryset = ExecucaoContrato.objects.all()
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


class EmpenhoSOFCacheFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name='anoEmpenho')

    class Meta:
        model = EmpenhoSOFCache
        fields = ['year']


class DownloadView(generics.ListAPIView):
    renderer_classes = [XLSXRenderer]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmpenhoSOFCacheFilter
    queryset = EmpenhoSOFCache.objects.all()
    serializer_class = EmpenhoSOFCacheSerializer

    def filter_queryset(self, queryset):
        if 'year' in self.request.query_params:
            self.year = self.request.query_params['year']
        else:
            self.year = date.today().year
            queryset = queryset.filter(anoEmpenho=self.year)
        return super().filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        filename = f'contratos_{self.year}.xlsx'

        headers = {
            'Content-Disposition': f'attachment; filename={filename}'
        }
        response = Response(serializer.data, headers=headers)
        return response
