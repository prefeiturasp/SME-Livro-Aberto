from django.contrib import admin

from .dao.models_dao import UnidadeValoresVerbaFromToDao
from .models import (
    PtrfFromToSpreadsheet,
    DistritoZonaFromToSpreadsheet,
    EtapaTipoEscolaFromToSpreadsheet,
    UnidadeRecursosFromToSpreadsheet,
    PtrfFromTo,
    DistritoZonaFromTo,
    EtapaTipoEscolaFromTo,
    UnidadeRecursosFromTo,
    Dre, UnidadeValoresVerbaFromToSpreadsheet, UnidadeValoresVerbaFromTo
)


@admin.register(PtrfFromToSpreadsheet)
class PtrfFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'year', 'extracted', 'created_at',
                    'added_fromtos', 'updated_fromtos')


@admin.register(DistritoZonaFromToSpreadsheet)
class DistritoZonaFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'extracted', 'created_at', 'added_fromtos',
                    'updated_fromtos')


@admin.register(EtapaTipoEscolaFromToSpreadsheet)
class EtapaTipoEscolaFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'extracted', 'created_at', 'added_fromtos',
                    'updated_fromtos')


@admin.register(UnidadeRecursosFromToSpreadsheet)
class UnidadeRecursosFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'year', 'extracted', 'created_at',
                    'added_fromtos', 'updated_fromtos')


@admin.register(UnidadeValoresVerbaFromToSpreadsheet)
class UnidadeValoresVerbaFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'year', 'extracted', 'created_at',
                    'added_fromtos', 'updated_fromtos')


@admin.register(PtrfFromTo)
class PtrfFromToAdmin(admin.ModelAdmin):
    list_display = ('year', 'codesc', 'vlrepasse')


@admin.register(DistritoZonaFromTo)
class DistritoZonaFromToAdmin(admin.ModelAdmin):
    list_display = ('coddist', 'zona')


@admin.register(EtapaTipoEscolaFromTo)
class EtapaTipoEscolaFromToAdmin(admin.ModelAdmin):
    list_display = ('tipoesc', 'desctipoesc', 'etapa')


@admin.register(UnidadeRecursosFromTo)
class UnidadeRecursosFromToAdmin(admin.ModelAdmin):
    list_display = ('year', 'codesc', 'grupo', 'subgrupo', 'valor', 'label')


@admin.register(UnidadeValoresVerbaFromTo)
class UnidadeValoresVerbaFromToAdmin(admin.ModelAdmin):
    list_display = ('year', 'codigo_escola', 'valor_mensal', 'verba_locacao',
                    'valor_mensal_iptu', 'situacao', 'data_do_encerramento')


@admin.register(Dre)
class DreAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
