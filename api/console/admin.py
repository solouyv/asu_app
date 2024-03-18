from django.contrib import admin
from .models import MainCommands, Subcommands, Devices


class SubCommandInline(admin.StackedInline):
    model = Subcommands


class MainCommandAdmin(admin.ModelAdmin):
    inlines = [SubCommandInline]


admin.site.register(MainCommands, MainCommandAdmin)
# admin.site.register(Subcommands)
admin.site.register(Devices)
