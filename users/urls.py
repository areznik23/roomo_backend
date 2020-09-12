from django.urls import path
from .views import *
from knox.views import LogoutView
urlpatterns = [
    
   path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutView.as_view(), name='knox_logout'),
    path('profile', user_profile)
]


