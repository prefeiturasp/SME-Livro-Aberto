from django.contrib import admin

from .models import (
    PtrfFromToSpreadsheet,
    DistritoZonaFromToSpreadsheet,
    EtapaTipoEscolaFromToSpreadsheet,
    UnidadeRecursosFromToSpreadsheet,
    PtrfFromTo,
    DistritoZonaFromTo,
    EtapaTipoEscolaFromTo,
    UnidadeRecursosFromTo,
)


@admin.register(PtrfFromToSpreadsheet)
class PtrfFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_fromtos', 'updated_fromtos')


@admin.register(DistritoZonaFromToSpreadsheet)
class DistritoZonaFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_fromtos', 'updated_fromtos')


@admin.register(EtapaTipoEscolaFromToSpreadsheet)
class EtapaTipoEscolaFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_fromtos', 'updated_fromtos')


@admin.register(UnidadeRecursosFromToSpreadsheet)
class UnidadeRecursosFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_fromtos', 'updated_fromtos')


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
