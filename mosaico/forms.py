from django import forms
from django.core.exceptions import ValidationError

from .models import MinimoLegalSpreadsheetModel


class MinimoLegalSpreadsheetAdminForm(forms.ModelForm):

    def clean(self):
        spreadsheet = self.cleaned_data.get('spreadsheet')
        spreadsheet_name = spreadsheet.name.replace(' ', '_')
        if MinimoLegalSpreadsheetModel.objects \
                .filter(spreadsheet__endswith=spreadsheet_name).exists():
            raise ValidationError('Planilha já importada')
        return self.cleaned_data
