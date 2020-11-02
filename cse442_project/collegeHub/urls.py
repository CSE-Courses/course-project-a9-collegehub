from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', views.login_request, name='login'),
    path('signup/', views.register, name='signup'),
    path('faq/', views.FAQ.as_view(), name='faq'),
    # path('home/', views.Home.as_view(), name='home'),

    path('section/<int:pk>', views.create_section, name='create-section'),
    path('specific/<int:pk>', views.create_specific, name='create-specific'),
    path('education/<int:pk>', views.create_education, name='create-education'),
    path('skill/<int:pk>', views.create_skill, name='create-skill'),
    path('profile/', views.profile, name='profile'),
    # path('register/', views.register, name='register'),
    path('specific', views.passer, name='specific-url'),
    path('test/', views.test_page.as_view(), name='test'),
    path('temp0/', views.temp0.as_view(), name='temp0'),
    path('temp1/', views.temp1.as_view(), name='temp1'),
    path('temp2/', views.temp2.as_view(), name='temp2'),
    path('temp3/', views.temp3.as_view(), name='temp3'),


    path('emailSent/', views.register_email_sent.as_view(), name="emailed"),
    path('emailConfirmed/', views.register_confirmed.as_view(), name="confirmed"),
    path('emaiNotConfirmed/', views.register_not_confirmed.as_view(), name="not_confirmed"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='templates/login.html'), name='login'),
    path('account/<slug:username>/', views.Account.as_view(), name='account'),
    path('settings/<slug:username>/', views.Settings.as_view(), name='settings'),
    path('logout/', auth_views.LogoutView.as_view(template_name='templates/logout.html'), name='logout'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "collegeHub/password_reset.html"), name = "reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "collegeHub/password_reset_sent.html"), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "collegeHub/password_reset_form.html"), name = "password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "collegeHub/password_reset_done.html"), name  = "password_reset_complete"),

    path('<slug:username>/', views.Index.as_view(), name='index'),



]
