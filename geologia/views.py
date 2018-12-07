from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from budget_execution.models import Execucao
from geologia.serializers import GeologiaSerializer


class GeologiaView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'geologia/base.html'
    queryset = Execucao.objects.all()
    serializer_class = GeologiaSerializer
