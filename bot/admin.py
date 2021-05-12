from django.contrib import admin

from .models import BotUser, Match, Log

# Register your models here.
admin.site.register(BotUser)
admin.site.register(Match)


class LogAdmin(admin.ModelAdmin):
    list_display = ('created_at',)


admin.site.register(Log, LogAdmin)
