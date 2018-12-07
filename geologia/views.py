from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from budget_execution.models import Execucao
from geologia import services


class GeologiaView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'geologia/base.html'
    queryset = Execucao.objects.all()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        gnd_data = services.prepare_gnd_data(qs)

        return Response({'gnd': gnd_data})
