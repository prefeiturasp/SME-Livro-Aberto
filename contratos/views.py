from datetime import date

from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from contratos.models import ExecucaoContrato
from contratos.serializers import ExecucaoContratoSerializer


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
        return serializer_class(*args, **kwargs)
