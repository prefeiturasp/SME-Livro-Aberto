from django.contrib import admin

from .models import (Deflator, DotacaoFromTo, GNDFromTo, FonteDeRecursoFromTo,
                     SubelementoFromTo)


@admin.register(Deflator)
class DeflatorAdmin(admin.ModelAdmin):
    pass


@admin.register(DotacaoFromTo)
class DotacaoFromToAdmin(admin.ModelAdmin):
    pass


@admin.register(GNDFromTo)
class GNDFromToAdmin(admin.ModelAdmin):
    pass


@admin.register(FonteDeRecursoFromTo)
class FonteDeRecursoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)


@admin.register(SubelementoFromTo)
class SubelementoFromToAdmin(admin.ModelAdmin):
    ordering = ('code',)
