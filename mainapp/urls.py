from django.urls import path
from .views import home,about, contact, games
import users.views as user_views

urlpatterns = [
    path('', home, name = 'home'),
    path('accounts/profile/', user_views.profile, name = 'profile'),
    path('about/us/', about, name = 'about'),
    path('contact/us/', contact, name = 'contact'),
    path('games/',games, name = 'games'),
]
