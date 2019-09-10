from model_mommy import mommy

from contratos.models import EmpenhoSOFCache


class TestEmpenhoSOFCacheModel:

    def test_indexer(self):
        emp = mommy.prepare(
            EmpenhoSOFCache, codModalidade=2, codElemento=3, codFonteRecurso=1,
            _fill_optional=True)

        expected = (
            f'{emp.anoEmpenho}.{emp.codOrgao}.{emp.codProjetoAtividade}.'
            f'{emp.codCategoria}.{emp.codGrupo}.0{emp.codModalidade}.'
            f'0{emp.codElemento}.0{emp.codFonteRecurso}'
        )

        assert expected == emp.indexer
