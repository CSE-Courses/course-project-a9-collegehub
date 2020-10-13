import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from collegeHub import models
from .forms import SignupForm, SpecificForm

from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
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
            'token':account_activation_token.make_token(user),
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
    if user is not None and account_activation_token.check_token(user, token):
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

def create_experience(user):
    experiences = models.Experiences(user=user)
    experiences.save()


def create_section(request):
    if request.method == 'POST':
        data = json.loads(request.read().decode())
        name = data['name']
        experience_id = int(data['experience_id'])

        experience = get_object_or_404(models.Experiences, pk=experience_id)
        section = models.Section(name=name, experiences=experience)
        section.save()

    return JsonResponse({'section_name':  name}, status=200)


def create_specific(request):
    if request.method == 'POST':
        form = SpecificForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form.cleaned_data.get('image')
            print(form.cleaned_data.get('description\n\n\n\n\n'))
            form.cleaned_data.get('bullet_section')
            form.cleaned_data.get('section')
        else:
            form = SpecificForm()

    return render(request, 'collegeHub/test.html', {'form': form})


class Index(TemplateView):
    template_name = 'collegeHub/index.html'


class Settings(TemplateView):
    template_name = 'collegeHub/settings.html'


class test_page(TemplateView):
    template_name = 'collegeHub/test.html'

    def get(self, request):
        form = SpecificForm(request.POST or None)
        context = {'form': form}
        return render(request, 'collegeHub/test.html', context)

    def post(self, request):
        return create_specific(request)
