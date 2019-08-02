from django.contrib import admin

from .models import ContratoCategoriaFromTo, ContratoCategoriaFromToSpreadsheet


@admin.register(ContratoCategoriaFromTo)
class ContratoCategoriaFromToAdmin(admin.ModelAdmin):
    list_display = ('indexer', 'categoria_name', 'categoria_desc')


@admin.register(ContratoCategoriaFromToSpreadsheet)
class ContratoCategoriaFromToSpreadsheeetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_fromtos', 'not_added_fromtos')
