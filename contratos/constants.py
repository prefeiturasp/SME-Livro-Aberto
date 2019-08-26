from django.conf import settings


CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT = settings.CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT  # noqa
CONTRATOS_RAW_DUMP_DIR_PATH = settings.CONTRATOS_RAW_DUMP_DIR_PATH
CONTRATOS_RAW_DUMP_FILENAME = settings.CONTRATOS_RAW_DUMP_FILENAME

CATEGORIA_FROM_TO_SLUG = {
    "Ações Culturais": "acoes-culturais",
    "Alimentação": "alimentacao",
    "Construções": "contrucoes",
    "Parcerias": "parcerias",
    "Pedagógico": "pedagogico",
    "Reformas e Manutenção": "manutencao",
    "Serviços Contínuos": "servicos",
    "Transporte": "transportes",
    "Uniforme e Material Escolar": "uniformes",
    "Outras Aquisições": "outros",
}
