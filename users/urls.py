from django.urls import path
from .views import *
from knox.views import LogoutView
urlpatterns = [ 
   path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutView.as_view(), name='knox_logout'),
    path('profile', update_profile),
    path('profile/gallery', create_gallery_image),
    path('messages/inbox', get_inbox),
    path('messages/sent', get_sent),
    path('messages', create_message),
    path('messages/reply', create_reply)
]


