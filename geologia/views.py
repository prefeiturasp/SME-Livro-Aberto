from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from budget_execution.models import Execucao
from geologia.serializers import GeologiaSerializer


class HomeView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'geologia/base.html'
    queryset = Execucao.objects.all()
    serializer_class = GeologiaSerializer

    def list(self, request):
        qs = self.get_queryset()
        programa_id = self.request.GET.get('programa_id', None)
        serializer = self.get_serializer(qs, programa_id=programa_id)
        return Response(serializer.data)
