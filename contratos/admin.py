from django.contrib import admin

from .models import ContratoCategoriaFromTo


@admin.register(ContratoCategoriaFromTo)
class ContratoCategoriaFromToAdmin(admin.ModelAdmin):
    list_display = ('indexer', 'categoria_name', 'categoria_desc')
