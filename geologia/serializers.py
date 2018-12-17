from django.db.models import Sum


class GeologiaSerializer:

    def __init__(self, queryset, programa_id=None, *args, **kwargs):
        self.queryset = queryset
        self._programa_id = int(programa_id) if programa_id else programa_id

    @property
    def data(self):
        return {
            'camadas': self.prepare_data(),
            'programa': self.prepare_data(programa_id=self._programa_id),
            'subfuncao': self.prepare_subfuncao_data(),
        }

    # Charts 1 and 2 (camadas and programa)
    def prepare_data(self, programa_id=None):
        qs = self.queryset

        ret = {
            'orcado': [],
            'empenhado': [],
        }

        # filtering for chart 2 (by programa)
        if programa_id:
            qs = qs.filter(programa_id=programa_id)
            ret['programa_id'] = programa_id

        years = qs.values('year').distinct()

        for year_dict in years:
            year = year_dict['year']
            year_qs = qs.filter(year=year)

            ret['orcado'].append(self._get_orcado_data_by_year(year_qs))
            ret['empenhado'].append(self._get_empenhado_data_by_year(year_qs))

        return ret

    def _get_orcado_data_by_year(self, qs):
        year = qs[0].year

        orcado_by_gnd = qs.values('gnd_gealogia__desc') \
            .annotate(orcado=Sum('orcado_atualizado'))
        orcado_total = qs.aggregate(total=Sum('orcado_atualizado'))
        orcado_total = orcado_total['total']

        orcado_gnds = self._get_orcado_gnds_list(orcado_by_gnd, orcado_total)

        return {
            "year": year.strftime("%Y"),
            "total": orcado_total,
            "gnds": orcado_gnds,
        }

    def _get_empenhado_data_by_year(self, qs):
        year = qs[0].year

        empenhado_by_gnd = qs.values('gnd_gealogia__desc') \
            .annotate(empenhado=Sum('empenhado_liquido'))
        empenhado_total = qs.aggregate(total=Sum('empenhado_liquido'))
        empenhado_total = empenhado_total['total']

        empenhado_gnds = self._get_empenhado_gnds_list(empenhado_by_gnd,
                                                       empenhado_total)

        return {
            "year": year.strftime("%Y"),
            "total": empenhado_total,
            "gnds": empenhado_gnds,
        }

    # Chart 3: Subfuncao
    def prepare_subfuncao_data(self):
        qs = self.queryset

        years = qs.values('year').distinct()

        ret = {
            'orcado': [],
            'empenhado': [],
        }
        for year_dict in years:
            year = year_dict['year']
            year_qs = qs.filter(year=year)

            ret['orcado'].append(self.get_subfuncao_year_orcado_data(year_qs))
            ret['empenhado'].append(
                self.get_subfuncao_year_empenhado_data(year_qs))

        return ret

    def get_subfuncao_year_orcado_data(self, qs):
        year = qs[0].year
        subfuncoes = qs.values('subfuncao_id').distinct()

        ret = {
            'year': year.strftime('%Y'),
            'subfuncoes': [],
        }

        for subfuncao in subfuncoes:
            qs_subfuncao = qs.filter(subfuncao=subfuncao['subfuncao_id'])
            ret['subfuncoes'].append(
                self.get_subfuncao_orcado_data(qs_subfuncao))

        return ret

    def get_subfuncao_year_empenhado_data(self, qs):
        year = qs[0].year
        subfuncoes = qs.values('subfuncao_id').distinct()

        ret = {
            'year': year.strftime('%Y'),
            'subfuncoes': [],
        }

        for subfuncao in subfuncoes:
            qs_subfuncao = qs.filter(subfuncao=subfuncao['subfuncao_id'])
            ret['subfuncoes'].append(
                self.get_subfuncao_empenhado_data(qs_subfuncao))

        return ret

    def get_subfuncao_orcado_data(self, qs):
        subfuncao = qs[0].subfuncao

        orcado_by_gnd = qs.values('gnd_gealogia__desc') \
            .annotate(orcado=Sum('orcado_atualizado'))
        orcado_total = qs.aggregate(total=Sum('orcado_atualizado'))
        orcado_total = orcado_total['total']

        orcado_gnds = self._get_orcado_gnds_list(orcado_by_gnd, orcado_total)

        return {
            "subfuncao": subfuncao.desc,
            "total": orcado_total,
            "gnds": orcado_gnds,
        }

    def get_subfuncao_empenhado_data(self, qs):
        subfuncao = qs[0].subfuncao

        empenhado_by_gnd = qs.values('gnd_gealogia__desc') \
            .annotate(empenhado=Sum('empenhado_liquido'))
        empenhado_total = qs.aggregate(total=Sum('empenhado_liquido'))
        empenhado_total = empenhado_total['total']

        empenhado_gnds = self._get_empenhado_gnds_list(empenhado_by_gnd,
                                                       empenhado_total)

        return {
            "subfuncao": subfuncao.desc,
            "total": empenhado_total,
            "gnds": empenhado_gnds,
        }

    def _get_orcado_gnds_list(self, orcado_by_gnd, orcado_total):
        return [
            {
                "name": gnd['gnd_gealogia__desc'],
                "value": gnd['orcado'],
                "percent": self._calculate_percent(
                    gnd['orcado'], orcado_total)
            }
            for gnd in orcado_by_gnd
        ]

    def _get_empenhado_gnds_list(self, empenhado_by_gnd, empenhado_total):
        return [
            {
                "name": gnd['gnd_gealogia__desc'],
                "value": gnd['empenhado'],
                "percent": self._calculate_percent(
                    gnd['empenhado'], empenhado_total),
            }
            for gnd in empenhado_by_gnd
        ]

    def _calculate_percent(self, value, total):
        if value is None or not total:
            return 0
        return value / total
