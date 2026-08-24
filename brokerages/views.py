from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignupForm


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    return render(request, 'brokerages/landing.html')


def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard:index')
    return render(request, 'brokerages/signup.html', {'form': form})
