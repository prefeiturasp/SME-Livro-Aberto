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

    def filter_queryset(self, queryset):
        if self.form.cleaned_data['dre']:
            self.form.cleaned_data['zona'] = ''
        if self.form.cleaned_data['distrito']:
            self.form.cleaned_data['dre'] = ''
        return super().filter_queryset(queryset)


class BaseListView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = EscolaInfoFilter
    template_name = 'regionalizacao/home.html'


class HomeView(BaseListView):
    queryset = EscolaInfo.objects.filter(budget_total__isnull=False)
    serializer_class = PlacesSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        level = 0
        if 'zona' in request.query_params:
            level = 1
        if 'dre' in request.query_params:
            level = 2
        if 'distrito' in request.query_params:
            level = 3
        serializer = self.get_serializer(queryset, level=level)

        return Response(serializer.data)
