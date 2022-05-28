from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Trading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0,verbose_name=('USDT'))
    profit = models.FloatField(default=0)
    sum =  models.FloatField(default=0)
    time_now = models.DateTimeField()
    due_time = models.DateTimeField()
    profited = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user}'

class RandUser(models.Model):
    count = models.IntegerField(default=0)
    views = models.IntegerField(default=0,null=True, blank=True)

class UserPayEvidence(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    evidence = models.ImageField(verbose_name = 'A photo of your payment Evidence',upload_to = 'media/payment_Evidence')
    date_upload = models.DateTimeField(auto_now=True)
    def get_total_evidence(self):
        return self.objects.all().count()
    
    # def save(self):
    #     super().save()
    #     img = Image.open(self.photo.path)
    #     if img.height > 300 or img.width >300:
    #         imageparam = (200, 200)
    #         img.thumbnail(imageparam)
    #         img.save(self.photo.path)
    #     if img.height < 300 or img.width < 300:
    #         imageparam = (200, 200)
    #         img.thumbnail(imageparam)
    #         img.save(self.photo.path)