from django.contrib import admin

from .models import CategoriaContratoFromTo, CategoriaContratoFromToSpreadsheet


@admin.register(CategoriaContratoFromTo)
class CategoriaContratoFromToAdmin(admin.ModelAdmin):
    list_display = ('indexer', 'categoria_name', 'categoria_desc')


@admin.register(CategoriaContratoFromToSpreadsheet)
class CategoriaContratoFromToSpreadsheeetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_fromtos', 'not_added_fromtos')
