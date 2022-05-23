from django.urls import path
from .views import (login,register, 
pre_profile,deposit,settings,user_profile,
my_transactions,trading, MakeInvestment,WithDraw
)
urlpatterns = [
    path('accounts/login/', login, name = 'login'),
    path('registrations/', register, name = 'register'),
    path('deposit/', deposit, name = 'deposit'),
    path('trading/chart/', trading, name = 'trading'),
    path('trade/usdt/', MakeInvestment.as_view(), name = 'trade'),
    path('my/account/profile/', user_profile, name = 'myprofile'),
    path('my/account/settings/', settings, name = 'settings'),
    path('my/account/transaction/', my_transactions, name = 'mytransactions'),
    path('post_registrations/<int:pk>/', pre_profile, name = 'pre_profile'),
    path('withdrow/income/', WithDraw.as_view(), name = 'withdrow'),
]
