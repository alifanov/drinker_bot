from django.db import models


# Create your models here.
class BotUser(models.Model):
    tg_id = models.CharField(max_length=256)
    is_open_for_requests = models.BooleanField(default=False)

    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    username = models.CharField(max_length=256, blank=True, null=True)
