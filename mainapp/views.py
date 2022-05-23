from django.shortcuts import render,redirect
from users.models import Mail,Account
from django.contrib import messages  
from django.utils  import timezone
import time
from .models import Trading, RandUser
import random
# Create your views here.

def home(request):
    if request.method =='POST':
        obj = Mail(
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            subject = request.POST['subject'],
            message = request.POST['message'],   
            )
        obj.save()
        messages.success(request,'Mail Sent!')
        return redirect ('/')
        
    user = RandUser.objects.all()
    all_views = RandUser.objects.get(id =1)
    all_views.views += 1
    all_views.save() 
    context = {
        'alluser':user[0],
        'tradeuser':user[0].count-27,
        'all_views':all_views,
    }

        
    return render(request,'mainapp/index-2.html',context)


def about(request):
    return render(request,'mainapp/about-us.html')

def contact(request):
    if request.method =='POST':
        obj = Mail(
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            subject = request.POST['subject'],
            message = request.POST['message'],   
            )
        obj.save()
        messages.success(request,'Mail Sent!')
        return redirect ('/')

    return render(request,'mainapp/contact.html')


def games(request):
    account,created = Account.objects.get_or_create(user = request.user)
    num = [ var for var in range(1,10)]
    amount = [var for var in range(1,6)]
    c = (3,4,5,6)
    numbers = set(random.sample(num, k=random.choice(c)))
    context = {
        'numbers':numbers,
        'amount':random.choice(amount),
        'account':account,
            }
    robot = random.choice(list(numbers))
    print(numbers,robot)
    if request.method =='POST':
        
        if int(account.balance) > int(request.POST['amount']):
            var = int(request.POST['choice'])
            gain = int(request.POST['amount'])
            if var == robot:
                msg = f'You Wone,The Number is {robot} as you gues'
                account.balance = account.balance + gain
                account.save()
                context.update({'msg':msg})
                return render(request,'dashboard/game.html',context)
            else:
                msg = f'Sorry You lose,The Number was {robot} but you choose {var}!'
                account.balance = account.balance - gain
                account.save()
                context.update({'msg':msg})
                return render(request,'dashboard/game.html',context)
        else:
            messages.info(request,'Your Balance is too low')
            return redirect('profile')

  
    return render(request, 'dashboard/game.html',context)