import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from collegeHub import models
from .forms import SpecificForm
from django.shortcuts import redirect
from djnago.contrib.auth.decorators import login_required
# Create your views here.


def register(user_request):
    if user_request.method == 'POST':
        form = UserCreationForm(user_request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(user_request, f'Account created for {username}- redirecting to login')
        else:
            form = UserCreationForm()
    return render(user_request, 'User/register.html',{'form':form})

@login_required
def profile(request):
    return render(request, 'templates\collegeHub/profile.html')

    

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
