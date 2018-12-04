from datetime import date

from rest_framework import generics

from budget_execution.models import Execucao
from mosaico.serializers import GrupoSerializer


class GrupoList(generics.ListAPIView):
    serializer_class = GrupoSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        return Execucao.objects.filter(year=date(year, 1, 1)) \
            .distinct('subgrupo__grupo')
