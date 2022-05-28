from multiprocessing import context
from django.shortcuts import render,redirect
from mainapp.forms import UserRegistrationForm
from .models import Profile,PinDeposit,Deposit,Account, Withdrowal
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView
from . import functions
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from mainapp.models import Trading, RandUser
from .import functions
from users import models
import datetime
from django.utils import timezone
# Create your views here.
def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request,user)
                    return redirect('profile')
                else:
                    msg = 'User records have issues, contact Admin!'
                    return render(request,'users/login.html', {'msg':msg})
            elif user is None:
                msg = 'Error in Login Credentials!'
                return render(request,'users/login.html', {'msg':msg})
            
        except Exception as err:
            return redirect('login')

    return render(request,'users/login.html')

def register(request):
    if request.method == 'POST':
        rand_user = RandUser.objects.get(id = 1)
        rand_user.count =  rand_user.count + int(functions.get_rand_user())
        rand_user.save()
        if User.objects.filter(email = request.POST['email']):
            msg = 'Email Already registered!'
            form = UserRegistrationForm(request.POST)
            context = {
                'form':form,
                'msg':msg,
            }
            return render(request,'users/register.html',context)

        else:   
            form = UserRegistrationForm(request.POST)
            try:
                if form.is_valid:
                    form.save()
                    username = form.cleaned_data.get('username')
                    user = User.objects.get(username = request.POST['username'])
                    profile = Profile( 
                        uid = functions.get_user_id(),
                        user = user

                    )
                    profile.save()
                    messages.success(request, 'Your registration was succesful!')
                    return redirect('pre_profile',user.id)          
            except ValueError:
                form = UserRegistrationForm(request.POST)
                msg = 'Error!'
                context = {
                    'form':form,
                    'msg':msg,
                        }
                return render(request,'users/register.html',context)
            except Exception as err:
                print('we have some issues', err)


    form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,'users/register.html',context)

def pre_profile(request,pk):
    if request.method == 'POST':
        user =User.objects.get(id = pk)
        obj = Profile.objects.get(user= user)
        obj.country = request.POST['country'] 
        obj.phone = request.POST['phone']
        obj.save()
        messages.success(request, 'Welcome!, Now Login')
        return redirect('login')
    return render(request,'users/country.html')

@login_required
def profile(request):
    if request.method =='POST':
        try:
            uid = request.POST['uid']
            userid = Profile.objects.get(uid = uid)
            if userid:
                acc = Profile.objects.get(user = request.user)
                acc.referrer = uid 
                acc.referred = True
                acc.profited = False
                acc.save()
                messages.info(request, 'Referer Added')
                return redirect('profile')
        except Exception:
            messages.info(request, 'No user with that ID')
            return redirect('profile')

    trade = Trading.objects.filter(user = request.user, profited = False)
    time = timezone.now()
    for item in trade:
        if time > item.due_time:
            item.profited = True
            print(item)
            account = Account.objects.get(user = item.user)
            account.balance = account.balance + item.sum
            account.save()
            item.save()

    try:
        deposit = Deposit.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
        withdrow = Withdrowal.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
        account = Account.objects.filter(user = User.objects.get(id = request.user.id))
        profile = Profile.objects.filter(user = User.objects.get(id = request.user.id))
        context = {
            'withdrow':withdrow,
            'deposit':deposit,
            'profile':profile[0],
            'account':account[0],
        }
        return render(request,'users/user_dashboard.html',context)

    except Exception:
        try:
            deposit = Deposit.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
            withdrow = Withdrowal.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
            account = Account.objects.filter(user = User.objects.get(id = request.user.id))
            context = {
                'withdrow':withdrow,
                'deposit':deposit,
                'account':account[0],
            }
            return render(request,'users/user_dashboard.html',context)
        except Exception:
            try:
                deposit = Deposit.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
                withdrow = Withdrowal.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
                profile = Profile.objects.filter(user = User.objects.get(id = request.user.id))
                context = {
                    'withdrow':withdrow,
                    'deposit':deposit,
                    'profile':profile[0],
                }
                return render(request,'users/user_dashboard.html',context)
        
            
            except Exception:
                return render(request,'users/user_dashboard.html')



def deposit(request):
    wallet = 'xadwqweewtrlwrtretewqrtert'

    if request.method =='POST':
        if float(request.POST['amount']) >49:
            try:
                obj = Deposit(
                    user = request.user,
                    amount = request.POST['amount'],
                    option = request.POST['method'],
                    date_deposited = timezone.now(),
                    )

                obj.save()
                messages.success(request,'Make your payment Using the Copied Wallet Address')
                messages.success(request,f'i do no copy?, Coppy it now! :{wallet}')
                return redirect('profile')
            except Exception as err:
                print('we have an Error :', err)
                pass
        else:
            messages.success(request,'Deposit must be aabove 50 USDT')
            return redirect('deposit')

    context = {
        'wallet':wallet,
    }
    return render(request,'users/deposit.html',context)


def settings(request):
    if request.method =='POST':
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            country = request.POST['country']
            wallet_address = request.POST['wallet_address']
            wallet_type = request.POST['wallet_type']
            user = User.objects.get(id = request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            profile = Profile.objects.get(user = request.user)
            profile.phone = phone
            profile.country =country
            profile.wallet_address = wallet_address
            profile.wallet_type = wallet_type
            user.save()
            profile.save()
            messages.success(request,'Your profile is updated succesfully!')
            return redirect('profile')
        except Exception as err:
            print('Something is not right: ', err)
            pass


    user = User.objects.filter(id=request.user.id)
    context = {
        'user':user[0],
    }
    return render(request,'users/settings.html',context)

def user_profile(request):
    
    return render(request,'users/myprofile.html')

def my_transactions(request):
    deposit_sum = Deposit.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
    account = Account.objects.filter(user=request.user).aggregate(sum = Sum('balance'))
    withdraw_sum = Withdrowal.objects.filter(user=request.user,approved =True).aggregate(sum = Sum('amount'))
            
    deposits = Deposit.objects.filter(user = request.user, approved =True).order_by('-date_approved')
    withdraws = Withdrowal.objects.filter(user = request.user, approved =True).order_by('-date_approved')
    context = {
        'withdraws':withdraws,
        'deposits':deposits,
        'deposit_sum':deposit_sum,
        'withdraw_sum':withdraw_sum,
        'account':account,
    }
    return render(request,'users/transactions.html',context)

def trading(request):
    return render(request,'users/tradingcharts.html') 


class MakeInvestment(LoginRequiredMixin,CreateView):
    model = Trading
    template_name = 'users/trades.html'
    success_url = '/accounts/profile/'
    fields = ['amount']
    def get_context_data(self, *args,**kwargs: any):
        context = super(MakeInvestment,self).get_context_data(*args,**kwargs)
        trade = Trading.objects.filter(user = self.request.user,profited = False).order_by('time_now').last()   
        others = Trading.objects.filter(user = self.request.user,profited = False).order_by('-time_now')    
        context.update({'trade':trade, 'others':others})
        return context 
    def form_valid(self, form):
        try:
            account = Account.objects.get(user = self.request.user)
            if account.balance > float(self.request.POST['amount']):
                if float(self.request.POST['amount']) > 50:
                    form.instance.user = self.request.user
                    now,due_time = functions.get_date()
                    interest = functions.get_percentage(self.request.POST['amount'])
                    form.instance.profit = interest
                    form.instance.sum = float(self.request.POST['amount']) + float(interest)
                    form.instance.time_now = now
                    form.instance.due_time = due_time 
                    account.balance = account.balance - float(self.request.POST['amount'])
                    account.save()
                    messages.success(self.request,'Success!!')
                    return super().form_valid(form) 
                else:
                    messages.info(self.request,'Trading Ammount must be above 50USDT')
                    return redirect('trade')
            else:
                messages.info(self.request,'Insufficient Account Balance, Pls Deposit')
                return redirect('trade')
        except Exception:
            messages.info(self.request,'It seems you Havent Deposited!')
            return redirect('trade')
def tradehistory(request):
    trades = Trading.objects.filter(user = request.user,profited = True)
    pending = Trading.objects.filter(user = request.user,profited = False)
    trades_sum = Trading.objects.filter(user = request.user,profited = True).aggregate(sum = Sum('profit'))
    context = {
        'trades':trades,
        'trades_sum':trades_sum,
        'pending':pending,
    }
    return render(request, 'users/tradehistory.html',context)

    
def all (request):
    return render(request,'users/alltrades.html')

def tradedetaileth (request):
    return render(request,'users/detail-trades.html')

def tradedetailbtc (request):
    return render(request,'users/tradedetailbtc.html')
def tradedetailcom (request):
    return render(request,'users/tradedetailcom.html')

def tradedetailforex(request):
    return render(request,'users/tradedetailforex.html')


def trades(request):
    if request.method == 'POST':

        try:
            account = Account.objects.get(user =request.user)
            if account.balance > float(request.POST['amount']):
                now,due_time = functions.get_date()
                interest = functions.get_percentage(request.POST['amount'])
                obj = Trading(
                user =request.user,
                amount = float(request.POST['amount']),
                profit = interest,
                sum = float(request.POST['amount']) + float(interest),
                time_now = now,
                due_time = due_time,
                    )

                account.balance = account.balance - float(request.POST['amount'])
                account.save()
                obj.save()
                messages.success(request,'Success!!')
                return  redirect('profile')  
            else:
                messages.info(request,'Insufficient Account Balance, Pls Deposit')
                return redirect('tradesucces')
        except Exception as err:
            print('error',err)
            messages.info(request,'It seems you havent Deposited!')
            return redirect('profile')

    return render(request,'users/confirm-trade.html')


def tradesbtc(request):
    if request.method == 'POST':

        try:
            account = Account.objects.get(user =request.user)
            if account.balance > float(request.POST['amount']):
                now,due_time = functions.get_date()
                interest = functions.get_percentage(request.POST['amount'])
                obj = Trading(
                user =request.user,
                amount = float(request.POST['amount']),
                profit = interest,
                sum = float(request.POST['amount']) + float(interest),
                time_now = now,
                due_time = due_time,
                    )

                account.balance = account.balance - float(request.POST['amount'])
                account.save()
                obj.save()
                messages.success(request,'Success!!')
                return  redirect('tradesucces')  
            else:
                messages.info(request,'Insufficient Account Balance, Pls Deposit')
                return redirect('profile')
        except Exception as err:
            print('error',err)
            messages.info(request,'It seems you havent Deposited!')
            return redirect('profile')

    return render(request,'users/confirmbtc.html')


def tradescom(request):
    if request.method == 'POST':

        try:
            account = Account.objects.get(user =request.user)
            if account.balance > float(request.POST['amount']):
                now,due_time = functions.get_date()
                interest = functions.get_percentage(request.POST['amount'])
                obj = Trading(
                user =request.user,
                amount = float(request.POST['amount']),
                profit = interest,
                sum = float(request.POST['amount']) + float(interest),
                time_now = now,
                due_time = due_time,
                    )

                account.balance = account.balance - float(request.POST['amount'])
                account.save()
                obj.save()
                messages.success(request,'Success!!')
                return  redirect('profile')  
            else:
                messages.info(request,'Insufficient Account Balance, Pls Deposit')
                return redirect('tradesucces')
        except Exception as err:
            print('error',err)
            messages.info(request,'It seems you havent Deposited!')
            return redirect('profile')

    return render(request,'users/confirmcom.html')


def tradesforex(request):
    if request.method == 'POST':

        try:
            account = Account.objects.get(user =request.user)
            if account.balance > float(request.POST['amount']):
                now,due_time = functions.get_date()
                interest = functions.get_percentage(request.POST['amount'])
                obj = Trading(
                user =request.user,
                amount = float(request.POST['amount']),
                profit = interest,
                sum = float(request.POST['amount']) + float(interest),
                time_now = now,
                due_time = due_time,
                    )

                account.balance = account.balance - float(request.POST['amount'])
                account.save()
                obj.save()
                messages.success(request,'Success!!')
                return  redirect('tradesucces')  
            else:
                messages.info(request,'Insufficient Account Balance, Pls Deposit')
                return redirect('profile')
        except Exception as err:
            print('error',err)
            messages.info(request,'It seems you havent Deposited!')
            return redirect('profile')

    return render(request,'users/confirmforex.html')
def tradesucces(request):
    return render(request, 'users/trade-success.html')

class MakePinDepositView(LoginRequiredMixin,CreateView):
    model = PinDeposit
    template_name = 'soanis/pay.html'
    success_url = '/soanis/'
    fields = ['amount']
    def form_valid(self, form):
        form.instance.admin = self.request.user.username
        pin = functions.make_new_deposit()
        form.instance.amount = float(self.request.POST['amount'])
        form.instance.pin = pin
        return super().form_valid(form)

class WithDraw(LoginRequiredMixin,CreateView):
    template_name = 'users/withdraw.html'
    model = Withdrowal
    fields = ['amount']
    success_url = '/accounts/profile/'
   
    def form_valid(self, form):
        pendings = Withdrowal.objects.filter(user  = self.request.user, approved = False, cancel = False)
        if not pendings:
            try:
                account = Account.objects.get(user = self.request.user)

                if float(self.request.POST['amount']) < float(account.balance):
                    if float(self.request.POST['amount'])>49.9:
                        if float(self.request.POST['amount'])<1001:
                            account.balance = account.balance - float(self.request.POST['amount'])
                            form.instance.user = self.request.user
                            form.instance.wallet_address = self.request.POST['wallet']
                            form.instance.amount = float(self.request.POST['amount'])
                            form.instance.date_placed = timezone.now()
                            account.save()
                            messages.success(self.request,'Your Withdrawal was placed Succesfully!')
                            return super().form_valid(form) 
                        else:
                            messages.info(self.request,'Withdrawal amount must be below or equal to 1000 USD')
                            return redirect('withdrow')
                    else:
                        messages.info(self.request,'Withdrawal amount must be above 50USD')
                        return redirect('withdrow')
                else:
                    messages.info(self.request,'Insufficient Balance, Pls Trade More')
                    return redirect('withdrow')
            except Exception:
                    messages.info(self.request,'Insufficient Balance, Pls Trade More')
                    return redirect('withdrow')          

        else:
            messages.info(self.request, 'Sorry!!,We are working on your Last Pending transaction')
            return redirect('withdrow')          

