from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))  # zůstat na stejné stránce


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')




def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Přihlášení bylo úspěšné')
            return redirect('home')
        else:
            messages.error(request, 'Neplatné přihlašovací údaje')
            # formulář zůstane otevřený díky proměnné
            return render(request, 'home.html', {'login_failed': True})

    return render(request, 'home.html')