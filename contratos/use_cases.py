from datetime import datetime


class GenerateExecucoesContratosUseCase:

    def __init__(self, empenhos_dao, execucoes_dao, modalidades_dao,
                 objetos_dao, fornecedores_dao):
        self.empenhos_dao = empenhos_dao
        self.execucoes_dao = execucoes_dao
        self.modalidades_dao = modalidades_dao
        self.objetos_dao = objetos_dao
        self.fornecedores_dao = fornecedores_dao

    def execute(self):
        for empenho in self.empenhos_dao.get_all():
            self._create_execucao_by_empenho(empenho=empenho)

    def _create_execucao_by_empenho(self, empenho):
        modalidade, _ = self.modalidades_dao.get_or_create(
            id=empenho.codModalidadeContrato,
            desc=empenho.txtDescricaoModalidadeContrato)
        objeto_contrato, _ = self.objetos_dao.get_or_create(
            desc=empenho.txtObjetoContrato)
        fornecedor, _ = self.fornecedores_dao.get_or_create(
            razao_social=empenho.txtRazaoSocial)

        execucao_data = {
            "cod_contrato": empenho.codContrato,
            "empenho_indexer": empenho.indexer,
            "year": datetime.strptime(str(empenho.anoEmpenho), "%Y"),
            "valor_empenhado": empenho.valEmpenhadoLiquido,
            "valor_liquidado": empenho.valLiquidado,
            "modalidade_id": modalidade.id,
            "objeto_contrato_id": objeto_contrato.id,
            "fornecedor_id": fornecedor.id,
        }
        return self.execucoes_dao.create(**execucao_data)
