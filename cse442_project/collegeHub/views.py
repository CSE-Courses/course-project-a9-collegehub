import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.urls import reverse, reverse_lazy
from collegeHub import models

from .forms import SignupForm, SpecificForm, SectionForm, EducationForm, UserProfileForm, UserEditForm
from .models import UserProfile, Experiences, Education
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import models as auth_models


# Create your views here.


def register(user_request):
    if user_request.method == 'POST':
        form = SignupForm(user_request.POST)
        p_form = UserProfileForm(user_request.POST)
        print(p_form)
        if form.is_valid():
            user = form.save(commit=False)
            profile = p_form.save(commit=False)

            if 'profile_pic' in user_request.FILES:
                print('got a picture')
                profile.profile_pic = user_request.FILES['profile_pic']
            if 'resume' in user_request.FILES:
                print('got a picture')
                profile.resume = user_request.FILES['resume']
                
            profile.user = user
            user.is_active = False
            new_user_experience = Experiences(profile = profile)

            user.save()
            profile.save()
            new_user_experience.save()

            current_site = get_current_site(user_request)
            mail_subject = 'Activate your account.'
            message = render_to_string('collegehub/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            print("here")
            # return HttpResponse('Please confirm your email address to complete the registration')
            return redirect(reverse('emailed'))  # add registration confirmation html
    else:
        form = SignupForm()
        p_form = UserProfileForm()
        return render(user_request, 'collegeHub/Signup.html', {'form': form, 'p_form':p_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return redirect(reverse('confirmed'))
    else:
        return redirect(reverse('not_confirmed'))


def EditProfile(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.user = user
            print(request.FILES)
            if 'profile_pic' in request.FILES:
                print('got a picture')
                profile.profile_pic = request.FILES['profile_pic']
            if 'resume' in request.FILES:
                print('got a picture')
                profile.resume = request.FILES['resume']
            user.save()
            profile.save()
            return redirect('index', username=request.user.username)
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
        user_form = UserEditForm(instance=request.user)

        return render(request, 'collegeHub/edit_profile.html', {'u_form': user_form,
                                                           'p_form': profile_form})


class register_email_sent(TemplateView):
    template_name = "collegehub/register_email_sent.html"


class register_confirmed(TemplateView):
    template_name = "collegehub/register_confirmed.html"


class register_not_confirmed(TemplateView):
    template_name = "collegehub/unconfirmed.html"


class Account(DetailView):
    model = models.UserProfile
    template_name = "collegehub/account.html"

    def get_object(self):
        username = self.kwargs.get('username')
        user = auth_models.User.objects.get(username=username)
        return get_object_or_404(models.UserProfile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        usr = auth_models.User.objects.get(username=username)
        userProfile = models.UserProfile.objects.get(user=usr)
        context['user_profile'] = userProfile
        return context


# class Signup(CreateView):
#     form_class = SignupForm
#     success_url = reverse_lazy('gsplit-login')

#     template_name = "collegehub/Signup.html"


# @login_required
def profile(request):
    return render(request, 'templates/profile.html')


# @login_required
def create_experience(user):
    experiences = models.Experiences(profile=user)
    experiences.save()


# @login_required
def create_section(request, pk):
    if request.method == 'POST':
        form = SectionForm(request.POST, request.FILES)
        if form.is_valid():

            name = form.data.get('name')
            new_section = form.save()

            experience = get_object_or_404(models.Experiences, pk=pk)
            new_section.experiences = experience
            new_section.save()

            return JsonResponse({'name': name, 'fail': False, 'section_pk': new_section.pk}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return


def passer(request):
    pass


# @login_required
def create_specific(request, pk):
    if request.method == 'POST':
        form = SpecificForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.data.get('image')
            description = form.data.get('description')
            bullet_section = form.data.get('bullet_section')
            position = form.data.get('position')
            company = form.data.get('company')
            link = form.data.get('link')
            new_specific = form.save()

            section = get_object_or_404(models.Section, pk=pk)
            new_specific.section = section
            new_specific.save()

            return JsonResponse(
                {'position': position, 'company': company,'link': link, 'description': description, 'bullet_section': bullet_section,
                 'section_pk': section.pk, 'fail': False, 'experience_pk': new_specific.pk},
                status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return

    # return JsonResponse({}, status=200)


# @login_required
def create_education(request, pk):
    if request.method == 'POST':
        form = EducationForm(request.POST, request.FILES)
        print('Form\'s valid:', form.is_valid())
        if form.is_valid():
            # image = form.data.get('image')
            institution = form.data.get('institution')
            certification_name = form.data.get('certification_name')
            description = form.data.get('description')
            month = form.data.get('month')
            year = form.data.get('year')
            new_education = form.save()

            userprofile = get_object_or_404(models.UserProfile, pk=pk)
            print('USER:', userprofile)
            new_education.profile = userprofile
            new_education.save()

            return JsonResponse(
                {'description': description, 'institution': institution, 'certification_name': certification_name,
                 'month': month, 'year': year, 'fail': False}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        form = EducationForm()
    return JsonResponse({}, status=200)


class Index(DetailView):
    model = models.UserProfile
    template_name = 'collegeHub/index.html'

    def get_object(self):
        username = self.kwargs.get('username')
        user = auth_models.User.objects.get(username=username)
        return get_object_or_404(models.UserProfile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        usr = auth_models.User.objects.get(username=username)
        userProfile = models.UserProfile.objects.get(user=usr)
        context['user_profile'] = userProfile
        experience = userProfile.experience
        context['experience'] = experience
        context['sectionForm'] = SectionForm()
        context['specificForm'] = SpecificForm()
        context['educationForm'] = EducationForm()
        return context


# def index(request, username):
#     userProfile = models.UserProfile.objects.get(username=username)
#     context = {'user_profile': userProfile, 'experience': userProfile.experience}
#     return render(template_name='collegeHub/index.html', context=context)


class Home(TemplateView):
    template_name = 'collegeHub/home.html'

class temp1(TemplateView):
    template_name = 'collegeHub/temp_1.html'

class FAQ(TemplateView):
    template_name = 'collegeHub/faq.html'


# @login_required
class Settings(DetailView):
    model = models.UserProfile
    template_name = 'collegeHub/settings.html'

    def get_object(self):
        username = self.kwargs.get('username')
        user = auth_models.User.objects.get(username=username)
        return get_object_or_404(models.UserProfile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        usr = auth_models.User.objects.get(username=username)
        userProfile = models.UserProfile.objects.get(user=usr)
        context['user_profile'] = userProfile
        return context


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password= password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in")
                print(request.user.username)
                return redirect('index', username=request.user.username)
            else:
                messages.error(request, "Not a valid username or password. Please try again or confirm your account.")
        else:
             messages.error(request, "Not a valid username or password")

    form = AuthenticationForm()
    return render(request,'collegeHub/login.html', {"form":form})

class test_page(TemplateView):
    template_name = 'collegeHub/test.html'

    def get(self, request):
        secForm = SectionForm()
        specForm = SpecificForm()
        eduForm = EducationForm()
        context = {'sectionForm': secForm, 'specificForm': specForm, 'educationForm': eduForm}
        return render(request, 'collegeHub/test.html', context)

