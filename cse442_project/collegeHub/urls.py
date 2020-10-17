from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('faq/', views.FAQ.as_view(), name='faq'),
    # path('home/', views.Home.as_view(), name='home'),
    path('section', views.create_section, name='create-section'),
    path('specific', views.create_specific, name='create-specific'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),

    path('test/', views.test_page.as_view(), name='test'),

    path('emailSent/', views.register_email_sent.as_view(), name="emailed"),
    path('emailConfirmed/', views.register_confirmed.as_view(), name="confirmed"),
    path('emaiNotConfirmed/', views.register_not_confirmed.as_view(), name="not_confirmed"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('login/', auth_views.LoginView.as_view(template_name='templates/login.html'), name='login'),
    path('<slug:username>/', views.Index.as_view(), name='index'),
    path('account/<slug:username>/', views.Account.as_view(), name='account'),
    path('settings/<slug:username>/', views.Settings.as_view(), name='settings'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='templates/logout.html'), name='logout'),



]
