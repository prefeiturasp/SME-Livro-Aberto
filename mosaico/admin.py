from django.contrib import admin

from .forms import MinimoLegalSpreadsheetAdminForm
from .models import MinimoLegalSpreadsheetModel


@admin.register(MinimoLegalSpreadsheetModel)
class MinimoLegalSpreadsheetAdmin(admin.ModelAdmin):
    form = MinimoLegalSpreadsheetAdminForm

    def get_changeform_initial_data(self, request):
        return {
            'title_25percent': 'DESPESAS COM AÇÕES TÍPICAS DE MDE',
            'limit_25percent': (
                '28- TOTAL DAS DESPESAS COM AÇÕES TÍPICAS DE MDE '
                '(22+23 + 24 + 25 + 26 + 27)'),
            'title_6percent': ('DESPESAS COM EDUCAÇÃO INCLUSIVA'),
            'limit_6percent': (
                '60-TOTAL COM DESPESAS COM AÇÕES TÍPICAS DO '
                'PROGRAMA DE EDUCAÇÃO INCLUSIVA (53+54+55+56+57+58+59)'
            ),
        }
