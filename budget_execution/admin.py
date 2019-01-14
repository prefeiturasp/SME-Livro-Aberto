from django.contrib import admin

from .models import GndGeologia


@admin.register(GndGeologia)
class GndGeologiaAdmin(admin.ModelAdmin):
    ordering = ('desc',)
    list_display = ('id', 'desc', 'slug')
