from django.contrib import admin, messages

from .models import (Deflator, DotacaoFromTo, DotacaoFromToSpreadsheet,
                     GNDFromTo, FonteDeRecursoFromTo,
                     SubelementoFromTo)


@admin.register(Deflator)
class DeflatorAdmin(admin.ModelAdmin):
    ordering = ('year',)
    list_display = ('year_str', 'index_number', 'variation_percent')

    def year_str(self, obj):
        return f'{obj.year.strftime("%Y")}'
    year_str.short_desc = 'Ano'


@admin.register(DotacaoFromTo)
class DotacaoFromToAdmin(admin.ModelAdmin):
    ordering = ('indexer',)
    list_display = ('indexer', 'grupo_code', 'grupo_desc',
                    'subgrupo_full_code', 'subgrupo_desc')

    def subgrupo_full_code(self, obj):
        return f'{obj.subgrupo_code} ({obj.grupo_code}.{obj.subgrupo_code})'
    subgrupo_full_code.short_desc = 'Código do Subgrupo'


@admin.register(DotacaoFromToSpreadsheet)
class DotacaoFromToSpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_fromtos', 'not_added_fromtos')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.added_fromtos:
            messages.info(
                request, f'Novos De-Paras adicionados: {obj.added_fromtos}')
        else:
            messages.error(request, 'Nenhum novo De-Para adicionado')

        if obj.not_added_fromtos:
            messages.error(
                request, ('De-Paras não adicionados pois já existiam no banco: '
                          f'{obj.not_added_fromtos}')
            )


@admin.register(GNDFromTo)
class GNDFromToAdmin(admin.ModelAdmin):
    ordering = ('gnd_code',)
    list_display = ('gnd_code', 'gnd_desc', 'elemento_code',
                    'elemento_desc', 'new_gnd_code',
                    'new_gnd_desc')


@admin.register(FonteDeRecursoFromTo)
class FonteDeRecursoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)
    list_display = ('code', 'name', 'grupo_code', 'grupo_name')


@admin.register(SubelementoFromTo)
class SubelementoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)
    list_display = ('code', 'desc', 'new_code', 'new_name')
