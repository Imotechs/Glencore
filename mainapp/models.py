from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Trading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name=('USDT'))
    profit = models.FloatField()
    sum =  models.FloatField()
    time_now = models.DateTimeField()
    due_time = models.DateTimeField()
    profited = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user}'

class RandUser(models.Model):
    count = models.IntegerField()
    views = models.IntegerField(null=True, blank=True)