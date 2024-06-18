from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Widok rejestracji użytkownika
def register(request):
    """
        Obsługuje formularz rejestracji użytkownika.
        Przyjmuje żądanie HTTP POST zawierające dane formularza `UserCreationForm`.
        Jeśli formularz jest poprawny, tworzy nowego użytkownika w bazie danych.
        Po zarejestrowaniu użytkownika, przekierowuje na stronę logowania.
        Returns:
            HttpResponse: Przekierowanie na stronę logowania po poprawnej rejestracji.
            Renderowanie strony z formularzem rejestracji w przypadku żądania GET.
        """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Ustawienie hasła
            user.save()
            messages.success(request, 'Registration successful.')  # Wiadomość sukcesu
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Widok logowania użytkownika
def user_login(request):
    """
        Obsługuje formularz logowania użytkownika.
        Przyjmuje żądanie HTTP POST zawierające dane formularza `AuthenticationForm`.
        Autentykuje użytkownika na podstawie podanych danych logowania.
        Po autentykacji, przekierowuje na stronę główną (`strona_glowna`).
        Returns:
            HttpResponse: Przekierowanie na stronę główną po poprawnym zalogowaniu.
            Renderowanie strony z formularzem logowania w przypadku żądania GET.
        """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)  # Autentykacja użytkownika
            if user is not None:
                login(request, user)
                return redirect('strona_glowna')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Widok wylogowania użytkownika
def user_logout(request):
    """
        Obsługuje wylogowanie użytkownika.
        Wylogowuje obecnego użytkownika i przekierowuje na stronę główną (`strona_glowna`).
        Returns:
            HttpResponse: Przekierowanie na stronę główną po wylogowaniu.
        """
    logout(request)
    return redirect('strona_glowna')
