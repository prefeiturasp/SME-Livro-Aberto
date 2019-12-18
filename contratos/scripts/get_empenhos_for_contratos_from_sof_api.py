from django.core.mail import mail_admins

from contratos import services


def run(*args):
    try:
        services.get_empenhos_for_contratos_from_sof_api()
    except Exception as e:
        subject = 'Erro ao atualizar os empenhos'
        msg = str(e)
        mail_admins(subject, msg)
        raise
