from django.contrib import admin

from .models import (Deflator, DotacaoFromTo, GNDFromTo, FonteDeRecursoFromTo,
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
    list_display = ('indexer', 'group_code', 'group_desc',
                    'subgroup_full_code', 'subgroup_desc')

    def subgroup_full_code(self, obj):
        return f'{obj.subgroup_code} ({obj.group_code}.{obj.subgroup_code})'
    subgroup_full_code.short_desc = 'Código do Subgrupo'


@admin.register(GNDFromTo)
class GNDFromToAdmin(admin.ModelAdmin):
    ordering = ('gnd_code',)
    list_display = ('gnd_code', 'gnd_desc', 'elemento_code',
                    'elemento_desc', 'new_gnd_code',
                    'new_gnd_desc')


@admin.register(FonteDeRecursoFromTo)
class FonteDeRecursoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)
    list_display = ('code', 'name', 'group_code', 'group_name')


@admin.register(SubelementoFromTo)
class SubelementoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)
    list_display = ('code', 'desc', 'new_code', 'new_name')
