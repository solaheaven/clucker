from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from microblogs.forms import SignUpForms, LogInForm
from django.contrib import messages
from django.core.cache import cache
"""view"""
def feed(request):
    return render(request, 'feed.html')
    
def home(request):
    return render(request, 'home.html')
    
def log_out(request):
    logout(request) 
    return redirect('home')


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_url = request.POST.get('next') or 'feed'
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    next = request.GET.get('next') or ''
    return render(request, 'log_in.html', {'form': form, 'next': next})


def sign_up(request):
    form = SignUpForms()
    if request.method == 'POST':
        form = SignUpForms(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForms()
    return render(request, 'sign_up.html', {'form':form})


