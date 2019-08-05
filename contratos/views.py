from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from contratos.models import ExecucaoContrato
from contratos.serializers import ExecucaoContratoSerializer


class HomeView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'contratos/home.html'
    queryset = ExecucaoContrato.objects.all()
    serializer_class = ExecucaoContratoSerializer
