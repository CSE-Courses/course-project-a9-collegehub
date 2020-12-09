import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django import forms as form_check
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, FormView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from collegeHub import models
from django.utils.timezone import make_aware

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.validators import validate_email
from .forms import UserProfileForm, UserEditForm
from .forms import SignupForm, SpecificForm, SectionForm, EducationForm, SkillForm, ProjectForm, EventForm, PostForm
from .forms import  DeleteSpecificForm, DeleteSectionForm, DeleteEducationForm, DeleteSkillForm, DeleteProjectForm, ChooseTemplateForm
from .models import UserProfile, Experiences, Education, Event, User, Post
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import json 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mass_mail
from django.contrib.auth import models as auth_models
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    DetailView
    #DeleteView
)
from .validators import validate_image, validate_pdf
from ics import Calendar
from ics import Event as eve
import tempfile
import io
import os

ACME_CHALLENGE_CONTENT = os.environ.get('ACME_CHALLENGE_CONTENT')
# Create your views here.

def acme_challenge(request):
    return HttpResponse(ACME_CHALLENGE_CONTENT)

def register(user_request):
    if user_request.method == 'POST':
        form = SignupForm(user_request.POST)
        p_form = UserProfileForm(user_request.POST)
        print(p_form)
        if form.is_valid():
            user = form.save(commit=False)
            profile = p_form.save(commit=False)
            if 'profile_pic' in user_request.FILES and validate_image(user_request.FILES['profile_pic']):
                print('got a picture')
                profile.profile_pic = user_request.FILES['profile_pic']
            if 'resume' in user_request.FILES and validate_image(user_request.FILES['resume']):
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
            message = render_to_string('collegeHub/acc_active_email.html', {
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
            # add registration confirmation html
            return redirect(reverse('emailed'))
        else:
            print(form.errors)
            return render(user_request, 'collegeHub/Signup.html', {'form': form, 'p_form':p_form})

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

        #
        # new_user_profile = UserProfile(user=user)
        # new_user_profile.save()
        #
        # new_user_experience = Experiences(profile=new_user_profile)
        # new_user_experience.save()


        # return redirect('home')
        return redirect(reverse('confirmed'))
    else:
        return redirect(reverse('not_confirmed'))

@login_required
def EditProfile(request):
    if request.method == "POST":
        if 'account' in request.POST:
            user_form = UserEditForm(request.POST, instance=request.user)
            if user_form.is_valid():
                print(user_form)
                user_form.data.get('')
                user_form.save()
                messages.success(request, "Successfully changed account")
                return redirect('account' )
            else:
                messages.error(request, 'Error : Please check all fields approriately')
                return redirect('account' )

        elif 'profile' in request.POST:
            print('received profile settings')
            profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
            if profile_form.is_valid():
                profile_info = profile_form.save(commit=False)
                if 'github.com' not in profile_form.cleaned_data.get('github'):
                    profile_info.github = ''
                else:
                    start_idx = profile_form.cleaned_data['github'].index('github.com')
                    profile_info.github = 'https://www.' + profile_form.cleaned_data['github'][start_idx:]
                profile_form.data.get('instagram')
                if 'instagram.com' not in profile_form.cleaned_data.get('instagram'):
                    profile_info.instagram = ''
                else:
                    start_idx = profile_form.cleaned_data['instagram'].index('instagram.com')
                    profile_info.linkedin = 'https://www.' + profile_form.cleaned_data['instagram'][start_idx:]
                if 'linkedin.com' not in profile_form.cleaned_data.get('linkedin'):
                    profile_info.linkedin = ''
                else:
                    start_idx = profile_form.cleaned_data['linkedin'].index('linkedin.com')
                    profile_info.linkedin = 'https://www.' + profile_form.cleaned_data['linkedin'][start_idx:]
                if 'facebook.com' not in profile_form.cleaned_data.get('facebook'):
                    profile_info.facebook = ''
                else:
                    start_idx = profile_form.cleaned_data['facebook'].index('facebook.com')
                    profile_info.facebook = 'https://www.' + profile_form.cleaned_data['facebook'][start_idx:]

                if 'profile_pic' in request.FILES and validate_image(request.FILES['profile_pic']):
                    print('got a picture')
                    profile_info.profile_pic = request.FILES['profile_pic']
                if 'resume' in request.FILES and validate_pdf(request.FILES['resume']):
                    print('got resume')
                    profile_info.resume = request.FILES['resume']

                profile_info.save()
                messages.success(request, "Successfully changed profile")
                return redirect('account' )
            else:
                messages.error(request, 'Error : Please check all fields approriately')
                return redirect('account' )
        # if user_form.is_valid():
        #     user = user_form.save(commit=False)
        #     profile = profile_form.save(commit=False)
        #     profile.user = user
        #     print(request.FILES)
        #     if 'profile_pic' in request.FILES:
        #         print('got a picture')
        #         profile.profile_pic = request.FILES['profile_pic']
        #     if 'resume' in request.FILES:
        #         print('got a picture')
        #         profile.resume = request.FILES['resume']
        #     user.save()
        #     profile.save()
        #     return redirect('index', username=request.user.username)
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
        user_form = UserEditForm(instance=request.user)
        url_form = str(request.user) + "." + str(get_current_site(request))
        return render(request, 'collegeHub/account.html', {'u_form': user_form,
                                                           'p_form': profile_form,
                                                           'url_form' : url_form.lower()})

def create_event(request):
    if request.method == "POST":
        event_form = EventForm(request.POST)
        print(event_form)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            profile = get_object_or_404(UserProfile, pk= request.user.userprofile.pk)
            print(event)

            c = Calendar()
            e = eve()
            e.name = event.title
            e.begin = event.start_time
            e.end = event.end_time
            e.organizer = request.user.first_name
            e.description = event.notes
            c.events.add(e)

            ics_file = io.StringIO()
            ics_file.writelines(c)

            event.user = profile
            print("sending email")
            current_site = get_current_site(request)
            email_subject = f'REMINDER: New event {event.title}'
            message = render_to_string('collegeHub/individual_scheduler.html', {
                'user': request.user,
                'domain': current_site.domain,
                'event': event
            })

            to_email = request.user.email
            email = EmailMessage(
                email_subject, message, to=[to_email]
            )
            email.attach('event.ics', ics_file.getvalue(), 'text/calendar')
            email.send()
            print(ics_file.getvalue())
            event.save()
            messages.success(request, 'You have created a new event')
            return redirect('events')
        else:
            messages.error(request, 'Something went wrong. Please try again.')
            return redirect('events')
    else:
        form = EventForm()
        return render(request, 'collegeHub/create_event.html', { 'form' : form})

class events(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'collegeHub/events.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        x =  queryset.filter(user__user__username__iexact=self.request.user.username)
        print(x)
        return x

class delete_event(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Event
    # template_name ='collegeHub/events.html'
    success_url = reverse_lazy('events')
    success_message = 'You have successfully deleted the event'

    def get_queryset(self):
        queryset = super().get_queryset()
        x =  queryset.filter(user__user__username__iexact=self.request.user.username)
        return x

    def get(self, request, *args, **kwargs):
        event_pk = kwargs.get('pk')
        event_obj = get_object_or_404(Event, pk=event_pk)
        current_site = get_current_site(request)
        email_subject = f'NOTICE: Event Deleted: {event_obj.title}'
        message = render_to_string('collegeHub/event_delete_email.html', {
            'user': request.user,
            'domain': current_site.domain,
            'event': event_obj
        })

        to_email = request.user.email
        email = EmailMessage(
            email_subject, message, to=[to_email]
        )
        email.send()     
        messages.success(self.request, 'You have successfully deleted the event')   
        return self.post(request, *args, **kwargs)

    
def group_invitation(request):
    if request.method == "POST":
        # print(request.POST)
        str_emails = request.POST.get('emails')
        emails = str_emails.split(',')
        event = {'title':  request.POST.get('title'), 'start_time' :  request.POST.get('start_time'), 'end_time':  request.POST.get('end_time'), 'notes':  request.POST.get('notes') }
        # print(emails)
        # print(event)
        
        event_obj = Event(user=request.user.userprofile, title=event['title'], start_time=event['start_time'], end_time= event['end_time'], notes=event['notes'], is_group=True)
        event_obj.save()
        email_event = event
        email_event['requester'] = request.user.email
        encoded_event = urlsafe_base64_encode(force_bytes(json.dumps(email_event)))


        cleaned_emails = []
        for em in emails:
            try:
                validate_email(em.strip())
                cleaned_emails.append(em)
            except form_check.ValidationError:
                print('invalid email.. ignoring')

        if cleaned_emails == []:
            messages.error(request, 'Something went wrong. Please try again')
            return redirect(reverse('events'))

        email_subject = 'REMINDER: New Group Event'
        
        message = render_to_string('collegeHub/group_scheduler.html', {
            'title' : event['title'],
            'start_time': event['start_time'],
            'end_time': event['end_time'],
            'notes': event['notes'],
            'domain' : get_current_site(request),
            'uid' : encoded_event,

            'requester': str(request.user.first_name + " " + request.user.last_name)
        })
        email_invite = ( email_subject, message, 'teamcollegeHub@gmail.com', cleaned_emails)
        send_mass_mail((email_invite,))
        messages.success(request, 'Invitations sent. The event has been added to your dashboard.')
        return redirect(reverse('events'))
    else:
        return render(request, 'collegeHub/group_email_form.html')

@login_required
def activate_invite(request, uidb64):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=request.user.pk)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None:
        print(user)
        print('event active')
        event = json.loads(uid)
        event_obj = Event(user=request.user.userprofile, title=event['title'], start_time=event['start_time'], end_time= event['end_time'], notes=event['notes'], is_group=True)
        event_obj.save()
        messages.success(request, 'You have accepted an invite')
        return redirect('events')
    else:
        messages.error(request, 'Something went wrong. Please try again or contact the host of the meeting.')
        return redirect('events')


class register_email_sent(TemplateView):
    template_name = "collegeHub/register_email_sent.html"


class register_confirmed(TemplateView):
    template_name = "collegeHub/register_confirmed.html"


class register_not_confirmed(TemplateView):
    template_name = "collegeHub/unconfirmed.html"




# class Account(LoginRequiredMixin, DetailView):
#     model = models.UserProfile
#     template_name = "collegeHub/account.html"

#     def get_object(self):
#         username = self.kwargs.get('username')
#         user = auth_models.User.objects.get(username=username)
#         return get_object_or_404(models.UserProfile, user=user)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         username = self.kwargs.get('username')
#         usr = auth_models.User.objects.get(username=username)
#         userProfile = models.UserProfile.objects.get(user=usr)
#         context['user_profile'] = userProfile
#         return context


# class Signup(CreateView):
#     form_class = SignupForm
#     success_url = reverse_lazy('gsplit-login')

#     template_name = "collegeHub/Signup.html"


@login_required
def profile(request):
    return render(request, 'templates/profile.html')


@login_required
def create_experience(user):
    experiences = models.Experiences(profile=user)
    experiences.save()


@login_required
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


@login_required
def create_project(request, pk):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # image = form.data.get('image')
            name = form.data.get('name')
            description = form.data.get('description')
            month = form.data.get('month')
            year = form.data.get('year')
            new_project = form.save()

            userprofile = get_object_or_404(models.UserProfile, pk=pk)
            new_project.profile = userprofile
            new_project.save()

            return JsonResponse(
                {'description': description, 'name': name,
                 'month': month, 'year': year, 'fail': False, 'project_pk': new_project.pk}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        form = ProjectForm()
    return JsonResponse({}, status=200)


@login_required
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
                {'position': position, 'company': company, 'link': link, 'description': description, 'bullet_section': bullet_section,
                 'section_pk': section.pk, 'fail': False, 'specific_pk': new_specific.pk},
                status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return

    # return JsonResponse({}, status=200)


@login_required
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
                 'month': month, 'year': year, 'fail': False, 'education_pk': new_education.pk}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        form = EducationForm()
    return JsonResponse({}, status=200)


class Index(DetailView):
    model = models.UserProfile
    template_name = 'collegeHub/base.html'

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
        context['skillForm'] = SkillForm()
        context['projectForm'] = ProjectForm()
        context['deleteSkillForm'] = DeleteSkillForm()
        context['deleteSectionForm'] = DeleteSectionForm()
        context['deleteProjectForm'] = DeleteProjectForm()
        context['deleteEducationForm'] = DeleteEducationForm()
        context['deleteEducationForm'] = DeleteSpecificForm()
        return context


# def index(request, username):
#     userProfile = models.UserProfile.objects.get(username=username)
#     context = {'user_profile': userProfile, 'experience': userProfile.experience}
#     return render(template_name='collegeHub/index.html', context=context)


@login_required
def create_skill(request, pk):
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES)
        if form.is_valid():

            skill_name = form.data.get('name')
            new_skill = form.save()

            user_profile = get_object_or_404(models.UserProfile, pk=pk)
            new_skill.profile = user_profile
            new_skill.save()

            return JsonResponse({'name': skill_name, 'fail': False, 'skill_pk': new_skill.pk}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return


class Home(TemplateView):
    template_name = 'collegeHub/home.html'

class search(TemplateView):
    template_name = 'collegeHub/search_profiles.html'

class temp0(TemplateView):
    template_name = 'collegeHub/temp_0.html'


class temp1(TemplateView):
    template_name = 'collegeHub/temp_1.html'

class temp2(TemplateView):
    template_name = 'collegeHub/temp_2.html'

class temp3(TemplateView):
    template_name = 'collegeHub/temp_3.html'

class FAQ(TemplateView):
    template_name = 'collegeHub/faq.html'

class cal(TemplateView):
    template_name = 'collegeHub/change_list.html'


class Settings(LoginRequiredMixin, DetailView):
    model = models.UserProfile
    template_name = 'collegeHub/settings.html'

    def get_object(self):
        username = self.request.user.username
        user = auth_models.User.objects.get(username=username)
        return get_object_or_404(models.UserProfile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        usr = auth_models.User.objects.get(username=username)
        userProfile = models.UserProfile.objects.get(user=usr)
        context['user_profile'] = userProfile
        context['chooseTemplateForm'] = ChooseTemplateForm
        return context


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"Logged in")
                print(request.user.username)
                return redirect('index', username=request.user.username)
            else:
                messages.error(
                    request, "Not a valid username or password. Please try again or confirm your account.")
        else:
            messages.error(request, "Not a valid username or password")

    form = AuthenticationForm()
    return render(request, 'collegeHub/login.html', {"form": form})


class error404(TemplateView):
    template_name = 'collegeHub/404error.html'

class test_page(TemplateView):
    template_name = 'collegeHub/test.html'

    def get(self, request):
        secForm = SectionForm()
        specForm = SpecificForm()
        eduForm = EducationForm()
        context = {'sectionForm': secForm,
                   'specificForm': specForm, 'educationForm': eduForm}
        return render(request, 'collegeHub/test.html', context)


@login_required
def delete_specific(request, pk):

    if request.method == 'POST':
        specific = get_object_or_404(models.Specific, id=pk)
        form = DeleteSpecificForm(request.POST)
        if form.is_valid():
            specific.delete()
            return JsonResponse({'fail': False}, status=200)
        return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def delete_section(request, pk):
    if request.method == 'POST':
        section = get_object_or_404(models.Section, id=pk)
        form = DeleteSectionForm(request.POST)
        if form.is_valid():
            section.delete()
            return JsonResponse({'fail': False}, status=200)
        return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def delete_education(request, pk):
    if request.method == 'POST':
        education = get_object_or_404(models.Education, id=pk)
        form = DeleteEducationForm(request.POST)
        if form.is_valid():
            education.delete()
            return JsonResponse({'fail': False}, status=200)
        return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def delete_skill(request, pk):
    if request.method == 'POST':
        skill = get_object_or_404(models.Skill, id=pk)
        form = DeleteSkillForm(request.POST)
        if form.is_valid():
            skill.delete()
            return JsonResponse({'fail': False}, status=200)
        return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def delete_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(models.Project, id=pk)
        form = DeleteProjectForm(request.POST)
        if form.is_valid():
            project.delete()
            return JsonResponse({'fail': False}, status=200)
        return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def edit_specific(request, pk):
    if request.method == 'POST':
        specific = get_object_or_404(models.Specific, id=pk)
        form = SpecificForm(request.POST, instance=specific)
        if form.is_valid():
            image = form.data.get('image')
            description = form.data.get('description')
            bullet_section = form.data.get('bullet_section')
            position = form.data.get('position')
            company = form.data.get('company')
            link = form.data.get('link')
            form.save()
            return JsonResponse(
                {'position': position, 'company': company, 'link': link, 'description': description,
                 'bullet_section': bullet_section, 'fail': False, 'specific_pk': specific.pk},
                status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def edit_section(request, pk):
    if request.method == 'POST':
        section = get_object_or_404(models.Section, id=pk)
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            name = form.data.get('name')

            form.save()
            return JsonResponse({'name': name, 'fail': False, 'section_pk': pk}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def edit_education(request, pk):
    if request.method == 'POST':
        education = get_object_or_404(models.Education, id=pk)
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            institution = form.data.get('institution')
            certification_name = form.data.get('certification_name')
            description = form.data.get('description')
            month = form.data.get('month')
            year = form.data.get('year')
            form.save()
            return JsonResponse(
                {'description': description, 'institution': institution, 'certification_name': certification_name,
                 'month': month, 'year': year, 'fail': False, 'education_pk': pk}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def edit_skill(request, pk):
    if request.method == 'POST':
        skill = get_object_or_404(models.Skill, id=pk)
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            name = form.data.get('name')
            form.save()
            return JsonResponse({'name': name, 'fail': False, 'skill_pk': pk}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def choose_template(request, temp):
    if request.method == 'POST':
        profile = models.UserProfile.objects.filter(user=request.user).first()
        form = ChooseTemplateForm(request.POST, instance=profile)
        if form.is_valid() and -1 < temp < 4:
            profile.template_number = temp
            profile.save()
            return JsonResponse({'temp_number': temp, 'fail': False}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return

@login_required
def edit_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(models.Project, id=pk)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            name = form.data.get('name')
            description = form.data.get('description')
            month = form.data.get('month')
            year = form.data.get('year')
            form.save()
            return JsonResponse({'name': name, 'fail': False, 'project_pk': pk,
                                 'description': description, 'month': month, 'year': year}, status=200)
        else:
            return JsonResponse({'fail': True}, status=200)
    else:
        return
@login_required
def create_blog(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        print(post_form)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            profile = get_object_or_404(UserProfile, pk= request.user.userprofile.pk)
            post.profile = profile
            post.save()
            print(post)
            return redirect('blog_all')
        else:
            return redirect('blog_create')
    else:
        form = PostForm()
        return render(request, 'collegeHub/create_blog.html', { 'form' : form})


class PostListView(ListView):
    model = Post
    template_name = 'collegeHub/blog_all.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(profile__user__username__iexact=self.request.user.username)
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'collegeHub/blog_detail.html'
    context_object_name = 'object'

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(profile__user__username__iexact=self.request.user.username)

class update_blog(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'collegeHub/edit_blog.html'
    fields = ['title', 'content']

    def get_success_url(self):
        return reverse('blog_all')

class delete_blog(LoginRequiredMixin, DeleteView):
    model = Post
    # template_name ='collegeHub/events.html'
    success_url = reverse_lazy('blog_all')

    def get_queryset(self):
        queryset = super().get_queryset()
        x =  queryset.filter(profile__user__username__iexact=self.request.user.username)
        return x

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)   


def SearchResult(request):
    if request.method == "POST":
        print(request.POST)
        query = request.POST.get('q')
        print(request)
        print('query is', query)
        if(len(query)==0):
            everything = models.UserProfile.objects.all()
            return render(request, 'collegeHub/search_profiles.html', {'results': everything})
        else:
            queries = str(query).split(' ')
            print(queries)
            querysett = []
            for q in queries:
                print('query is ',q)
                unames = models.UserProfile.objects.filter(user__username__icontains=q)
                fnames = models.UserProfile.objects.filter(user__first_name__icontains=q)
                lnames = models.UserProfile.objects.filter(user__last_name__icontains=q)
                fullquery = unames | fnames | lnames

                querysett+=fullquery.distinct()
            
            print(querysett)

            return render(request, 'collegeHub/search_profiles.html', {'results': list(set(querysett))})
    else:
        return render(request, 'collegeHub/search_profiles.html', {'results': '0'})