from django.contrib import admin

from .models import (Deflator, DotacaoFromTo, GNDFromTo, FonteDeRecursoFromTo,
                     SubelementoFromTo)


@admin.register(Deflator)
class DeflatorAdmin(admin.ModelAdmin):
    pass


@admin.register(DotacaoFromTo)
class DotacaoFromToAdmin(admin.ModelAdmin):
    ordering = ('indexer',)


@admin.register(GNDFromTo)
class GNDFromToAdmin(admin.ModelAdmin):
    ordering = ('gnd_code',)


@admin.register(FonteDeRecursoFromTo)
class FonteDeRecursoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)


@admin.register(SubelementoFromTo)
class SubelementoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)
