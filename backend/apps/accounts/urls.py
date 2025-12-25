from django.urls import path
from . import views
from django.contrib.auth import views as auth
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name ='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name ='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    path('register-success/', views.registration_success, name='registration_success'),

    # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
    
]