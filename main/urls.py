from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name= 'home'),
    path('home', views.home, name= 'home'),
    path('sign-up', views.sign_up, name= 'sign-up'),
    path('post', views.create_post, name='post')
]