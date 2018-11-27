from django.contrib import admin

from .models import (Deflator, DotacaoFromTo, GNDFromTo, FonteDeRecursoFromTo,
                     SubelementoFromTo)


@admin.register(Deflator)
class DeflatorAdmin(admin.ModelAdmin):
    ordering = ('year',)
    list_display = ('year_str', 'index_number', 'variation_percent')

    def year_str(self, obj):
        return f'{obj.year.strftime("%Y")}'
    year_str.short_description = 'Ano'


@admin.register(DotacaoFromTo)
class DotacaoFromToAdmin(admin.ModelAdmin):
    ordering = ('indexer',)
    list_display = ('indexer', 'group_code', 'group_description',
                    'subgroup_full_code', 'subgroup_description')

    def subgroup_full_code(self, obj):
        return f'{obj.subgroup_code} ({obj.group_code}.{obj.subgroup_code})'
    subgroup_full_code.short_description = 'Código do Subgrupo'


@admin.register(GNDFromTo)
class GNDFromToAdmin(admin.ModelAdmin):
    ordering = ('gnd_code',)
    list_display = ('gnd_code', 'gnd_description', 'elemento_code',
                    'elemento_description', 'new_gnd_code',
                    'new_gnd_description')


@admin.register(FonteDeRecursoFromTo)
class FonteDeRecursoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)
    list_display = ('code', 'name', 'group_code', 'group_name')


@admin.register(SubelementoFromTo)
class SubelementoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)
    list_display = ('code', 'description', 'new_code', 'new_name')
