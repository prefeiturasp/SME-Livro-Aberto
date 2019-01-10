from django.contrib import admin

from .models import GndGealogia


@admin.register(GndGealogia)
class GndGealogiaAdmin(admin.ModelAdmin):
    ordering = ('desc',)
    list_display = ('id', 'desc', 'slug')
