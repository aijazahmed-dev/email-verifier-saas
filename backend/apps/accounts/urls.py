from django.urls import path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('register/', views.register, name ='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name ='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    
]