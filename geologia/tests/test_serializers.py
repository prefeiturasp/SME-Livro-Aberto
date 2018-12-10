from datetime import date
from decimal import Decimal

from model_mommy import mommy

from budget_execution.models import Execucao
from geologia.serializers import GeologiaSerializer


class TestGeologiaSerializer:

    def test_prepare_gnd_data(self):
        pass
        # execucoes_2017 = mommy.make(
        #     Execucao,
        #     year=date(2017, 1, 1),
        #     _quantity=2)
        # execucoes_2018 = mommy.make(
        #     Execucao,
        #     year=date(2018, 1, 1),
        #     _quantity=2)

        # execucoes = Execucao.objects.all()
        # serializer = GeologiaSerializer(execucoes)
        # ret = serializer.prepare_gnd_data()

        # orcado_2017 = sum([e.orcado_atualizado for e in execucoes_2017])
        # orcado_2018 = sum([e.orcado_atualizado for e in execucoes_2018])
        # # expected

        # empenhado_2017 = sum([e.empenhado_liquido for e in execucoes_2017])
        # empenhado_2018 = sum([e.empenhado_liquido for e in execucoes_2018])

    def test_get_orcado_gnds_list(self):
            gnds = [
                {'gnd_gealogia__desc': 'gnd1', 'orcado': Decimal(10)},
                {'gnd_gealogia__desc': 'gnd2', 'orcado': Decimal(20)},
                {'gnd_gealogia__desc': 'gnd3', 'orcado': Decimal(30)},
            ]
            orcado_total = {'total': Decimal(60)}

            expected = [
                {
                    "name": gnd['gnd_gealogia__desc'],
                    "value": gnd['orcado'],
                    "percent": gnd['orcado'] / orcado_total['total']
                }
                for gnd in gnds
            ]

            serializer = GeologiaSerializer([])
            ret = serializer._get_orcado_gnds_list(
                gnds, orcado_total)

            assert expected == ret

    def test_get_empenhado_gnds_list(self):
            gnds = [
                {'gnd_gealogia__desc': 'gnd1', 'empenhado': Decimal(10)},
                {'gnd_gealogia__desc': 'gnd2', 'empenhado': Decimal(20)},
                # must support None for empenhado
                {'gnd_gealogia__desc': 'gnd3', 'empenhado': None},
            ]
            empenhado_total = {'total': Decimal(30)}

            expected = []
            for gnd in gnds:
                if gnd['empenhado'] is None:
                    gnd['empenhado'] = 0

                expected.append({
                    "name": gnd['gnd_gealogia__desc'],
                    "value": gnd['empenhado'],
                    "percent": gnd['empenhado'] / empenhado_total['total']
                })

            serializer = GeologiaSerializer([])
            ret = serializer._get_empenhado_gnds_list(
                gnds, empenhado_total)

            assert expected == ret
