import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from collegeHub import models
from .forms import SpecificForm, SectionFrom, EducationFrom
from django.shortcuts import redirect
# Create your views here.


def register(user_request):
    if user_request.method == 'POST':
        form = UserCreationForm(user_request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            return redirect(reverse_lazy('index')) # add registration confirmation html
    else:
        form = UserCreationForm()
        return render(user_request, 'collegeHub/registerTest.html',{'form':form})
    

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
            form.save()
        else:
            form = SpecificForm()
    else:
        form = SpecificForm()

    return JsonResponse({}, status=200)


#@login_required
def create_education(request):
    if request.method == 'POST':
        form = SpecificForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
