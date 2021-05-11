from django.contrib import admin

from .models import BotUser, Match

# Register your models here.
admin.site.register(BotUser)
admin.site.register(Match)
