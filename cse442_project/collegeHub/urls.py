from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm, SetPasswordForm
from .views import (
    PostListView,
    PostDetailView
)

urlpatterns = [
    path(r'^.well-known/acme-challenge/.*$', views.acme_challenge, name='acme-challenge'),
    path('', views.Home.as_view(), name='home'),
    path('login/', views.login_request, name='login'),
    path('signup/', views.register, name='signup'),
    path('faq/', views.FAQ.as_view(), name='faq'),
    path('cal/', views.cal.as_view(), name='calendar'),
    # path('home/', views.Home.as_view(), name='home'),

    path('section/<int:pk>', views.create_section, name='create-section'),
    path('specific/<int:pk>', views.create_specific, name='create-specific'),
    path('education/<int:pk>', views.create_education, name='create-education'),
    path('skill/<int:pk>', views.create_skill, name='create-skill'),
    path('project/<int:pk>', views.create_project, name='create-project'),
    path('deleteEducation/<int:pk>', views.delete_education, name='delete-education'),
    path('deleteSection/<int:pk>', views.delete_section, name='delete-section'),
    path('deleteSpecific/<int:pk>', views.delete_specific, name='delete-specific'),
    path('deleteSkill/<int:pk>', views.delete_skill, name='delete-skill'),
    path('deleteProject/<int:pk>', views.delete_project, name='delete-project'),
    path('editEducation/<int:pk>', views.edit_education, name='edit-education'),
    path('editSection/<int:pk>', views.edit_section, name='edit-section'),
    path('editSpecific/<int:pk>', views.edit_specific, name='edit-specific'),
    path('editSkill/<int:pk>', views.edit_skill, name='edit-skill'),
    path('editProject/<int:pk>', views.edit_project, name='edit-project'),
    path('chooseTemplate/<int:temp>', views.choose_template, name='choose-template'),

    path('profile/', views.profile, name='profile'),
    path('specific', views.passer, name='specific-url'),
    path('test/', views.test_page.as_view(), name='test'),
    path('Red_Marble/', views.temp0.as_view(), name='temp0'),
    path('Purple_Candy/', views.temp1.as_view(), name='temp1'),
    path('Subtle_Blue/', views.temp2.as_view(), name='temp2'),
    path('Book/', views.temp3.as_view(), name='temp3'),
    path('404/', views.error404.as_view(), name='404'),
    # path('Search/', views.search.as_view(), name='Search'),

    path('emailSent/', views.register_email_sent.as_view(), name="emailed"),
    path('emailConfirmed/', views.register_confirmed.as_view(), name="confirmed"),
    path('emaiNotConfirmed/', views.register_not_confirmed.as_view(), name="not_confirmed"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activate_event/<uidb64>/', views.activate_invite, name='activate_event'),

    path('login/', auth_views.LoginView.as_view(template_name='templates/login.html'), name='login'),
    path('account/', views.EditProfile, name='account'),
    path('settings/', views.Settings.as_view(), name='settings'),
    path('logout/', auth_views.LogoutView.as_view(template_name='templates/logout.html'), name='logout'),

    #path('blog_create/', views.create_blog, name = 'blog_create'),
    path('blogs/', PostListView.as_view() , name = 'blog_all'),
    path('blogs_create/', views.create_blog , name = 'blog_create'),
    path('blogs/delete/<int:pk>', views.delete_blog.as_view(), name = 'delete_blog' ),
    path('blogs/update/<int:pk>', views.update_blog.as_view(), name = 'edit_blog' ),
    path('blogs/<int:pk>/', PostDetailView.as_view() , name = 'blog_detail'),
    path('Search/', views.SearchResult, name='Search'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "collegeHub/password_reset.html",form_class=UserPasswordResetForm), name = "reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "collegeHub/password_reset_sent.html"), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( template_name = "collegeHub/password_reset_form.html", form_class=SetPasswordForm), name = "password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "collegeHub/password_reset_done.html"), name  = "password_reset_complete"),
    path('create_event/', views.create_event, name  = "create_event"),
    path('events/', views.events.as_view(), name  = "events"),
    path('events/delete/<int:pk>', views.delete_event.as_view(), name='delete_event'),
    path('group_email/', views.group_invitation, name='group_email'),
    path('<slug:username>/', views.Index.as_view(), name='index'),
]
