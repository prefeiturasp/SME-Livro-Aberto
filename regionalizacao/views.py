from copy import deepcopy
from datetime import date

from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from regionalizacao.models import EscolaInfo
from regionalizacao.serializers import PlacesSerializer


class EscolaInfoFilter(filters.FilterSet):
    zona = filters.CharFilter(field_name='distrito__zona')
    dre = filters.CharFilter(field_name='dre__code')
    distrito = filters.NumberFilter(field_name='distrito__coddist')
    escola = filters.CharFilter(field_name='escola__codesc')
    year = filters.NumberFilter()

    def filter_queryset(self, queryset):
        if not self.form.cleaned_data['year']:
            self.form.cleaned_data['year'] = date.today().year

        query_params = deepcopy(self.form.cleaned_data)

        if self.form.cleaned_data['dre']:
            self.form.cleaned_data['zona'] = ''
        if self.form.cleaned_data['distrito']:
            self.form.cleaned_data['dre'] = ''
        map_qs = super().filter_queryset(queryset)

        self.form.cleaned_data['zona'] = ''
        self.form.cleaned_data['dre'] = ''
        self.form.cleaned_data['distrito'] = ''
        self.form.cleaned_data['escola'] = ''
        locations_qs = super().filter_queryset(queryset)
        return query_params, map_qs, locations_qs


class HomeView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = EscolaInfoFilter
    template_name = 'regionalizacao/home.html'
    queryset = EscolaInfo.objects.filter(budget_total__isnull=False)
    serializer_class = PlacesSerializer

    def list(self, request, *args, **kwargs):
        query_params, map_qs, locations_qs = self.filter_queryset(
            self.get_queryset())

        level = 0
        if 'zona' in request.query_params:
            level = 1
        if 'dre' in request.query_params:
            level = 2
        if 'distrito' in request.query_params:
            level = 3
        if 'escola' in request.query_params:
            level = 4

        locations_graph_type = request.query_params.get('localidade', 'zona')
        serializer = self.get_serializer(
            map_queryset=map_qs, locations_queryset=locations_qs, level=level,
            query_params=query_params,
            locations_graph_type=locations_graph_type)

        return Response(serializer.data)
