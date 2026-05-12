from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignupForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

    context = {
        'form': form
    }
    return render(request, 'users/signup.html', context)


def dashboard_view(request):
    return render(request, 'users/dashboard.html')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'