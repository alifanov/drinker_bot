from django.db import models


# Create your models here.
class BotUser(models.Model):
    tg_id = models.CharField(max_length=256)
    # is_open_for_requests = models.BooleanField(default=False)
    open_for_requests_until = models.DateTimeField(null=True, blank=True)

    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    username = models.CharField(max_length=256, blank=True, null=True)

    def get_username(self):
        return self.username if self.username else f'{self.first_name} {self.last_name}'


class Match(models.Model):
    requester_tg_id = models.PositiveIntegerField()
    responder_tg_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()
