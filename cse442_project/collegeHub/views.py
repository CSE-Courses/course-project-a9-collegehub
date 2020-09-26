from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import initRegisterForm

# Create your views here.
def register(user_request):
    if user_request.method == 'POST':
        form = initRegisterForm(user_request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(user_request, f'Account created for {username}')
        else:
            form = initRegisterForm()
    return render(user_request, 'User/register.html',{'form':form})
    


