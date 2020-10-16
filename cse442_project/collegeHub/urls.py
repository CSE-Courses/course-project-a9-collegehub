from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('settings', views.Settings.as_view(), name='settings'),
    path('section', views.create_section, name='create-section'),
    path('specific', views.create_specific, name='create-specific'),
    path('test/', views.test_page.as_view(), name='test'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view('templates/login.html'), name='login'),
    path('logout/', auth_views.Logout.as_view('templates/logout.html'), name='logout'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "collegeHub/password_reset.html"), name = "reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "collegeHub/password_reset_sent.html"), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "collegeHub/password_reset_form.html"), name = "password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "collegeHub/password_reset_done.html"), name  = "password_reset_complete"),


    path('profile/', auth_views.profile, name='profile')



    
    

]
