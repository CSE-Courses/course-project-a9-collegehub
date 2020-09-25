from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def register(user_request):
    if user_request.method == 'POST':
        form = UserCreationForm(user_request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(user_request, f'Account created for {email}')
        else:
            form = UserCreationForm()
    return render(user_request, 'User/register.html',{'form':form})
    


