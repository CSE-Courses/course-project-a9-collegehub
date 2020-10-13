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
    path('emailSent/', views.register_email_sent.as_view(), name="emailed"),
    path('emailConfirmed/', views.register_confirmed.as_view(), name="confirmed"),
    path('emaiNotConfirmed/', views.register_not_confirmed.as_view(), name="not_confirmed"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view('templates/login.html'), name='login'),
    path('logout/', auth_views.Logout.as_view('templates/logout.html'), name='logout'),
    path('profile/', auth_views.profile.as_view(), name='profile'),

]
