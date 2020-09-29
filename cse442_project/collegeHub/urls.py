from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('settings', views.Settings.as_view(), name='settings'),
    path('section', views.create_section, name='create-section'),
    path('specific', views.create_specific, name='create-specific'),
    path('test/', views.test_page.as_view(), name='test'),
    path('register/', views.register, name='register')

]
