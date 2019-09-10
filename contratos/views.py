import os

from datetime import date

from django.http import HttpResponse, Http404
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from contratos.constants import GENERATED_XLSX_PATH
from contratos.models import ExecucaoContrato, CategoriaContrato
from contratos.serializers import ExecucaoContratoSerializer


class ExecucaoContratoFilter(filters.FilterSet):
    year = filters.AllValuesFilter(field_name='year__year', empty_label=None)
    category = filters.ModelChoiceFilter(
        queryset=CategoriaContrato.objects.all(), field_name='categoria',
        empty_label='Todas categorias')

    def __init__(self, data=None, queryset=None, *args, **kwargs):
        super().__init__(data=data, queryset=queryset, *args, **kwargs)
        if 'year' not in self.data:
            ordered = queryset.order_by('-year__year')
            year = ordered.values_list('year__year', flat=True).first()

            data = self.data.copy()
            data['year'] = year
            self.data = data

    class Meta:
        model = ExecucaoContrato
        fields = ['year', 'category']


class FilteredTemplateHTMLRenderer(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        data = super().get_template_context(data, renderer_context)
        view = renderer_context['view']
        request = renderer_context['request']

        filter_backend = view.filter_backends[0]()
        qs = view.get_queryset()
        filterset = filter_backend.get_filterset(request, qs, view)
        data['filter_form'] = filterset.form

        return data


class HomeView(generics.ListAPIView):
    renderer_classes = [FilteredTemplateHTMLRenderer, JSONRenderer]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ExecucaoContratoFilter
    # TODO: add view tests
    queryset = ExecucaoContrato.objects.filter(categoria__isnull=False)
    serializer_class = ExecucaoContratoSerializer
    template_name = 'contratos/home.html'

    def get_serializer(self, qs_category_filtered, *args, **kwargs):
        original_qs = self.queryset
        year = self.request.GET.get('year')
        # TODO: refactor it. couldn't find a way to avoid repeating this code
        if not year:
            ordered = qs_category_filtered.order_by('-year__year')
            year = ordered.values_list('year__year', flat=True).first()
        qs_year_filtered = self.filterset_class(dict(year=year), original_qs).qs

        serializer_class = self.get_serializer_class()
        return serializer_class(qs_year_filtered, qs_category_filtered)


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
