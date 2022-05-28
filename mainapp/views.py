from django.shortcuts import render,redirect
from users.models import Mail,Account
from django.contrib import messages  
from django.utils  import timezone
from django.views.generic import CreateView
import time
from .models import Trading, RandUser,UserPayEvidence
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

    c = (3,2,4,5)
    numbers = set(random.sample(num, k=random.choice(c)))
    context = {
        'numbers':numbers,
        'amount':random.choice(amount),
        'account':account,
            }
    robot = random.choice(list(numbers))
    if request.method =='POST':
        rnumber = request.POST['rnumbers']
        gain = int(request.POST['amount'])
        rnumber_rpl = rnumber.replace("{","")
        rnumber_rpls = rnumber_rpl.replace("}","")
        rnumber_join = ''.join( ch for ch in rnumber_rpls if ch.isalnum())
        print(random.choice(list(rnumber_join)))
        if float(account.balance) >= float(request.POST['amount']):
            var = int(request.POST['choice'])
            numz =  random.choice(list(rnumber_join))
            if var == int(numz):
                print(var,numz)
                msg = f'You Won!,you guess right!!'
                account.balance = float(account.balance) + float(gain*2)
                account.save()
                context.update({'msg':msg})
                return render(request,'dashboard/game.html',context)
            else:
                msg = f'Sorry You lose!,The Number should have been\n {numz} but you choose {var}!'
                account.balance = account.balance - gain
                account.save()
                context.update({'msg':msg})
                return render(request,'dashboard/game.html',context)
        else:
            messages.info(request,'Your Balance is too low')
            return redirect('profile')

  
    return render(request, 'dashboard/game.html',context)

class EvidenceView(CreateView):
    model = UserPayEvidence
    success_url = ('/accounts/profile/')
    template_name = 'mainapp/evidence.html'
    fields = ['evidence']
    def form_valid(self,form):
        form.instance.user = self.request.user
        messages.success(self.request,'Uploaded!')
        return super().form_valid(form)


def game2(request):
    account,created = Account.objects.get_or_create(user = request.user)
    num = [ ch for ch in range(999,9999)]
    amount = [i for i in range(1,6)]
    c = (2,2)
    numbers = set(random.sample(num, k=random.choice(c)))
    context = {
        'numbers':numbers,
        'amount':random.choice(amount),
        'account':account,
            }
    robot = int(random.choice(list(numbers)))
    if request.method =='POST':
        prev_numbers = request.POST.get('numbers')

        if int(account.balance) > int(request.POST['amount']):
            var = int(request.POST['choice'])
            gain = float(request.POST['amount'])*2
            choices =  prev_numbers.replace("{","")
            choic = choices.replace("}","")
            ok = choic.split(',')
            print(numbers,ok)
            print(var)
            print(prev_numbers,)
            if var ==robot:
                msg = f'You Won!,you guess right!!'
                account.balance = account.balance + gain
                account.save()
                context.update({'msg':msg}) 
                return render(request,'dashboard/game2.html',context)
            else:
                msg = f'Sorry You lose!,The Number should have been\n {robot} but you choose {var}!'
                account.balance = account.balance - gain
                account.save()
                context.update({'msg':msg})
                return render(request,'dashboard/game2.html',context)
        else:
            messages.info(request,'Your Balance is too low')
            return redirect('profile')

  
    return render(request, 'dashboard/game2.html',context)
