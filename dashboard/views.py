from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,CreateView,DetailView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from mainapp.models import  Trading, UserPayEvidence
from users.models import Deposit,PinDeposit,Profile,Withdrowal,Mail,Account
from django.db.models import Sum
from django.contrib import messages
from users import functions
from django.utils import timezone
from email.message import EmailMessage
import smtplib
from django.conf import settings

mail_username = settings.EMAIL_HOST_USER
mail_password = settings.EMAIL_HOST_PASSWORD
# Create your views here.

class Dashboard(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
  model = User
  template_name = 'dashboard/index.html'

  def get_context_data(self, *args, **kwargs):
    context =super(Dashboard,self).get_context_data( *args, **kwargs)
    users =  User.objects.all().order_by('-date_joined')
    Tdeposits = Deposit.objects.filter(approved =True).aggregate(sum = Sum('amount'))
    deposits = Deposit.objects.filter(approved =True).order_by('-date_approved')
    withdraws = Withdrowal.objects.filter(approved =True).aggregate(sum = Sum('amount'))   
    trades = Trading.objects.filter(profited =True)  
    admins =  User.objects.filter(is_superuser = True).order_by('-date_joined')
    staffs =  User.objects.filter(is_staff = True).order_by('-date_joined')
    mails = Mail.objects.filter(seen= False)
    context.update({'Tdeposits':Tdeposits,'trades':trades,'users':users,'withdraws':withdraws,'deposits':deposits, 'mails':mails,'staffs':staffs, 'admins':admins})
    return context
  def test_func(self):
    if self.request.user.is_superuser or self.request.user.is_staff:
      return True
    return False

class deposit(TemplateView):
    deposits =  Deposit.objects.filter(approved=True,cancel=False).order_by('-date_approved')
    withdraws =  Withdrowal.objects.filter(approved=True,cancel=False).order_by('-date_approved')
    
# class Staffs(UserPassesTestMixin,ListView ):
#     model = User
#     template_name = 'dashboard/staffs.html'

#     def get_context_data(self, *args,**kwargs: any):
#         context = super(Staffs,self).get_context_data(*args,**kwargs)
#         mails = Mail.objects.filter(seen= False)
#         staffs = User.objects.filter(is_staff = True, is_superuser=True).order_by('-date_joined')
#         context.update({'staffs':staffs,'mails':mails})
#         return context 

#     def post(self,request,*args, **kwargs):
#         if request.method =='POST':
#             username = request.POST['search'].strip()
#             print(username)
#             try:
#                 users = User.objects.get(username = username)
#                 return render(request,'dashboard/staffs.html',{'users':users})

#             except Exception as er:
#                 print('we have an erro:', er)
#                 try:
#                     email = User.objects.get(email = username)
#                     return render(request,'dashboard/staffs.html',{'users':email})
#                 except Exception as err:
#                     print('we have an erro:', err)
#                     messages.info(request,'No such User')
#                     return redirect('staffs')


#     def test_func(self):
#         if self.request.user.is_superuser:
#             return True
#         return False



class AllUsers(UserPassesTestMixin,ListView ):
    model = User
    template_name = 'dashboard/reg-users.html'
    paginate_by = 5
    context_object_name = 'users'
    ordering = ['-date_joined']
    def get_context_data(self, *args,**kwargs: any):
        context = super(AllUsers,self).get_context_data(*args,**kwargs)
        mails = Mail.objects.filter(seen= False)
        context.update({ 'mails':mails})
        return context 
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class AllDeposit(UserPassesTestMixin,ListView ):
    model = Deposit
    template_name = 'dashboard/deposits.html'
    paginate_by = 5
    def get_context_data(self, *args,**kwargs: any):
        context = super(AllDeposit,self).get_context_data(*args,**kwargs)
        deposits = Deposit.objects.filter(approved= False, cancel = False)
        context.update({ 'deposits':deposits})
        return context
    def post(self,request,*args, **kwargs):
        if request.method =='POST':
            
            try:
                id = request.POST['approve']
                deposit = Deposit.objects.get(id = int(id))
                obj,created = Account.objects.get_or_create(user = deposit.user)
                obj.balance = float(obj.balance)  + deposit.amount 
                obj.save()
                deposit.approved = True
                deposit.date_approved = timezone.now()
                deposit.save()

                refer = Profile.objects.filter(user = deposit.user,referred = True,profited = False)
                if refer:
                    referrer = Profile.objects.filter(uid = refer[0].referrer)
                    referrer_account,created = Account.objects.get_or_create(user = referrer[0].user)
                    referrer_account.balance =referrer_account.balance + float(functions.get_referrer_percentage(deposit.amount))
                    referrer_account.save() 
                    refer[0].profited = True
                    refer[0].save()
                    areferrer = Profile.objects.filter(uid = 123456789)
                    areferrer_account,created = Account.objects.get_or_create(user = areferrer[0].user)
                    areferrer_account.balance = areferrer_account.balance + float(functions.get_referrer_percentage(deposit.amount))
                    areferrer_account.save() 
                    messages.info(request,'Approved!')
                    return redirect('deposits')
                else:
                    areferrer = Profile.objects.filter(uid = 123456789)
                    areferrer_account,created = Account.objects.get_or_create(user = areferrer[0].user)
                    areferrer_account.balance = areferrer_account.balance + float(functions.get_referrer_percentage(deposit.amount))
                    areferrer_account.save() 
                    messages.info(request,'Approved!')
                    return redirect('deposits')
            except Exception as err:
                print("we heve an error", err)
                id = request.POST['cancel']
                deposit = Deposit.objects.get(id = int(id))
                deposit.cancel = True
                deposit.date_approved = timezone.now()
                deposit.save()
                messages.info(request,'Canceled!')
                return redirect('deposits')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class AllWithdraws(UserPassesTestMixin,ListView ):
    model = Deposit
    template_name = 'dashboard/withdrawals.html'
    paginate_by = 10
    def get_context_data(self, *args,**kwargs: any):
        context = super(AllWithdraws,self).get_context_data(*args,**kwargs)
        withdraws = Withdrowal.objects.filter(approved= False, cancel = False)
        context.update({ 'withdraws':withdraws})
        return context
    def post(self,request,*args, **kwargs):
        if request.method =='POST':
            
            try:
                id = request.POST['approve']
                withdraw = Withdrowal.objects.get(id = int(id))
                obj,created = Account.objects.get_or_create(user = withdraw.user)
                obj.balance = float(obj.balance)  - withdraw.amount 
                obj.save()
                withdraw.approved = True
                withdraw.date_approved = timezone.now()
                withdraw.save()
                messages.info(request,'Approved!')
                return redirect('withdraws')
            except Exception:
                id = request.POST['cancel']
                withdow = Withdrowal.objects.get(id = int(id))
                withdow.cancel = True
                withdow.date_approved = timezone.now()
                withdow.save()
                messages.info(request,'Canceled!')
                return redirect('withdraws')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class Emails(UserPassesTestMixin,ListView ):
    model = Mail
    template_name = 'dashboard/email-inbox.html'
    def get_context_data(self, *args,**kwargs: any):
        context = super(Emails,self).get_context_data(*args,**kwargs)
        mails = Mail.objects.filter(seen = False).order_by('-id')
        context.update({'mails':mails})
        return context    
    def post(self,request,*args, **kwargs):
        if request.method =='POST':
            try:
                id = request.POST['mail']
                mail = Mail.objects.get(id = int(id))
                mail.seen = True
                mail.save()
                return redirect('mails')
            except Exception:
                return redirect('mails')
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

class ViewEmails(UserPassesTestMixin,DetailView):
    model = Mail
    template_name = 'dashboard/email-read.html'


    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False



class MakeMail(UserPassesTestMixin,TemplateView ):
    model = Mail
    template_name = 'dashboard/email-compose.html'
    def post(self,request,*args, **kwargs):
        if request.method =='POST':
            try:
                email = request.POST['email']
                subject =request.POST['subject']
                body =request.POST['message']
                msg = EmailMessage()
                msg['To'] = email  
                msg['subject'] = subject
                msg['From'] =f'no-reply<{mail_username}>'
                msg.set_content(body)
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(mail_username, mail_password)
                        smtp.send_message(msg)
                        messages.success(request,'Mail Sent Succesfully!')
                        return redirect('sendmails')
                except Exception as error:
                    messages.info(request, f'Error : {error}')
                    return redirect('sendmails')

            except Exception as err:
                print('there is errrrro: ',err)
                return redirect('mails')
    def test_func(self):
        if self.request.user.is_superuser  or self.request.user.is_staff:
            return True
        return False

class ActiveTrades(UserPassesTestMixin,ListView):
    model = Trading
    context_object_name= 'trades'
    template_name = 'dashboard/active-trades.html'
    paginate_by = 10

    ordering = ['-time_now']
    def get_queryset(self):
        return Trading.objects.filter(profited = False).order_by('-time_now')
    def test_func(self):
        if self.request.user.is_superuser  or self.request.user.is_staff:
            return True
        return False

class SuccessfulTrades(UserPassesTestMixin,ListView):
    model = Trading
    context_object_name= 'trades'
    template_name = 'dashboard/successful-trades.html'
    paginate_by = 10

    def get_queryset(self):
        return Trading.objects.filter(profited = True).order_by('-due_time')
    def test_func(self):
        if self.request.user.is_superuser  or self.request.user.is_staff:
            return True
        return False

class AdminUploadView(UserPassesTestMixin,ListView):
    model = UserPayEvidence
    template_name = 'dashboard/evidence.html'
    context_object_name = 'uploads'
    paginate_by = 2
    ordering = ['-date_upload']
 
    def test_func(self):
        if self.request.user.is_superuser  or self.request.user.is_staff:
            return True
        return False
# class Pin(UserPassesTestMixin,CreateView):
#     model = PinDeposit
#     fields = ['amount']
#     template_name = 'dashboard/generate-pin.html'
#     def form_valid(self, form):
#         form.instance.staff = self.request.user
#         form.instance.pin = functions.make_new_deposit()
#         messages.success(self.request, 'Pin Generated Pls Copy')
#         return   super().form_valid(form)
#     def test_func(self):
#         if self.request.user.is_superuser  or self.request.user.is_staff:
#             return True
#         return False


# class PinDetail(UserPassesTestMixin,DetailView):
#     model = PinDeposit
#     template_name = 'dashboard/pin_detail.html'
#     def test_func(self):
#         if self.request.user.is_superuser  or self.request.user.is_staff:
#             return True
#         return False

# class PintPayments(UserPassesTestMixin,ListView):
#     model = PinDeposit
#     context_object_name= 'deposits'
#     template_name = 'dashboard/pin-deposits.html'
#     def test_func(self):
#         if self.request.user.is_superuser  or self.request.user.is_staff:
#             return True
#         return False