from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from budget_execution.models import Execucao
from geologia.serializers import GeologiaSerializer


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

class SobreView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'geologia/sobre.html'
    queryset = Execucao.objects.filter(subgrupo__isnull=False)
    serializer_class = GeologiaSerializer

    def list(self, request):
        qs = self.get_queryset()
        subfuncao_id = self.request.GET.get('subfuncao_id', None)
        serializer = self.get_serializer(qs, subfuncao_id=subfuncao_id)
        return Response(serializer.data)
