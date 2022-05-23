from django.contrib import admin
from .models import Profile,Withdrowal,Deposit,PinDeposit,Account,Mail
# Register your models here.
admin.site.register(Profile)
admin.site.register(Withdrowal)
admin.site.register(Deposit)
admin.site.register(PinDeposit)
admin.site.register(Account)
admin.site.register(Mail)
