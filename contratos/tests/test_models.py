from model_mommy import mommy

from contratos.models import EmpenhoSOFCache


class TestEmpenhoSOFCacheModel:

    def test_indexer(self):
        emp = mommy.prepare(EmpenhoSOFCache, _fill_optional=True)

        expected = (
            f'{emp.anoEmpenho}.{emp.codOrgao}.{emp.codProjetoAtividade}.'
            f'{emp.codCategoria}.{emp.codGrupo}.{emp.codModalidade}.'
            f'{emp.codElemento}.{emp.codFonteRecurso}.'
            f'{emp.codSubElemento}'
        )

        assert expected == emp.indexer
