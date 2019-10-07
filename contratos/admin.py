from django.contrib import admin

from .models import (
    CategoriaContrato, CategoriaContratoFromTo,
    CategoriaContratoFromToSpreadsheet, EmpenhoSOFCache, EmpenhoSOFCacheTemp,
    EmpenhoSOFFailedAPIRequest)


@admin.register(CategoriaContratoFromTo)
class CategoriaContratoFromToAdmin(admin.ModelAdmin):
    list_display = ('indexer', 'categoria_name', 'categoria_desc')


@admin.register(CategoriaContratoFromToSpreadsheet)
class CategoriaContratoFromToSpreadsheeetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_fromtos', 'not_added_fromtos')


@admin.register(CategoriaContrato)
class CategoriaContratoAdmin(admin.ModelAdmin):
    ordering = ('desc',)
    list_display = ('id', 'name', 'slug', 'desc')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(EmpenhoSOFCache)
class EmpenhoSOFCacheAdmin(admin.ModelAdmin):
    list_display = ('indexer', 'codContrato', 'anoExercicioContrato',
                    'anoEmpenho')


@admin.register(EmpenhoSOFCacheTemp)
class EmpenhoSOFCacheTempAdmin(admin.ModelAdmin):
    list_display = ('indexer', 'codContrato', 'anoExercicioContrato',
                    'anoEmpenho')


@admin.register(EmpenhoSOFFailedAPIRequest)
class EmpenhoSOFFailedAPIRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'error_code', 'created_at')
