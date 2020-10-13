import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from collegeHub import models

from .forms import SignupForm, SpecificForm, SectionFrom, EducationFrom

from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Create your views here.


def register(user_request):
    if user_request.method == 'POST':
        form = SignupForm(user_request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(user_request)
            mail_subject = 'Activate your account.'
         

            message = render_to_string('collegehub/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user),
                })
            
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(   
                        mail_subject, message, to=[to_email]
            )
            email.send()
            print("here")
            # return HttpResponse('Please confirm your email address to complete the registration')
            return redirect(reverse('emailed')) # add registration confirmation html
    else:
        form = SignupForm()
        return render(user_request, 'collegeHub/registerTest.html',{'form':form})
    
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

class register_email_sent(TemplateView):
    template_name = "collegehub/register_email_sent.html"

class register_confirmed(TemplateView):
    template_name = "collegehub/register_confirmed.html"

class register_not_confirmed(TemplateView):
    template_name = "collegehub/unconfirmed.html"

#@login_required
def create_experience(user):
    experiences = models.Experiences(profile=user)
    experiences.save()


#@login_required
def create_section(request):
    if request.method == 'POST':
        form = SectionFrom(request.POST, request.FILES)
        if form.is_valid():
            name = form.data.get('name')
            form.save()
            return JsonResponse({'name': name, 'fail': False}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return


#@login_required
def create_specific(request):
    if request.method == 'POST':
        form = SpecificForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.data.get('image')
            description = form.data.get('description')
            bullet_section = form.data.get('bullet_section')
            section = form.data.get('section')
            form.save()
            return JsonResponse({'description': description, 'bullet_section': bullet_section, 'section':section, 'fail': False}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return

    # return JsonResponse({}, status=200)


#@login_required
def create_education(request):
    if request.method == 'POST':
        form = SpecificForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            image = form.data.get('image')
            location = form.data.get('location')
            certification_name = form.data.get('certification_name')
            description = form.data.get('description')
            month = form.data.get('month')
            year = form.data.get('year')
            form.save()
            return JsonResponse({'description': description, 'location': location, 'certification_name':certification_name, 'month': month, 'year': year, 'fail': False}, status=200)
        else:
            form = EducationFrom()
    else:
        form = EducationFrom()
    return JsonResponse({}, status=200)


class Index(TemplateView):
    template_name = 'collegeHub/index.html'


#@login_required
class Settings(TemplateView):
    template_name = 'collegeHub/settings.html'


class test_page(TemplateView):
    template_name = 'collegeHub/test.html'

    def get(self, request):
        secForm = SectionFrom(request.POST or None)
        specForm = SpecificForm(request.POST or None)
        eduForm = EducationFrom(request.POST or None)
        context = {'sectionForm': secForm, 'specificForm': specForm, 'educationForm': eduForm}
        return render(request, 'collegeHub/test.html', context)

    def post(self, request):
        form = SectionFrom(request.POST, request.FILES)
        if form.is_valid():
            return create_section(request)
        form = SpecificForm(request.POST, request.FILES)
        if form.is_valid():
            return create_specific(request)
        form = EducationFrom(request.POST, request.FILES)
        if form.is_valid():
            return create_education(request)
        return
