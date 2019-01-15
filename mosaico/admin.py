from django.contrib import admin

from .models import MinimoLegalSpreadsheetModel


@admin.register(MinimoLegalSpreadsheetModel)
class MinimoLegalSpreadsheetAdmin(admin.ModelAdmin):

    def get_changeform_initial_data(self, request):
        return {
            'title_25percent': 'DESPESAS COM AÇÕES TÍPICAS DE MDE',
            'limit_25percent': 'TOTAL DAS DESPESAS COM AÇÕES TÍPICAS DE MDE',
            'title_6percent': ('DESPESAS COM AÇÕES TÍPICAS DO PROGRAMA DE '
                               'EDUCAÇÃO INCLUSIVA'),
            'limit_6percent': (
                '60-TOTAL COM DESPESAS COM AÇÕES TÍPICAS DO '
                'PROGRAMA DE EDUCAÇÃO INCLUSIVA (53+54+55+56+57+58+59)'
            ),
        }
