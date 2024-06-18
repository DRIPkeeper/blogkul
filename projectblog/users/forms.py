from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

# Formularz tworzenia użytkownika
class UserCreationForm(forms.ModelForm):
    """
        Formularz służący do tworzenia nowego użytkownika.
        Pola:
        - email: Adres email użytkownika.
        - firstname: Imię użytkownika.
        - lastname: Nazwisko użytkownika.
        - phone: Numer telefonu użytkownika.
        - password1: Hasło użytkownika (wprowadzone).
        - password2: Potwierdzenie hasła użytkownika.
        Metody:
        - clean_password2: Waliduje, czy hasła w polach 'password1' i 'password2' są takie same.
        - save: Zapisuje użytkownika do bazy danych, ustawiając jego hasło.
        Zwraca:
        - Obiekt User: Zwraca zapisanego użytkownika.

        """
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Potwierdzenie hasła', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'phone')

    # Walidacja potwierdzenia hasła
    def clean_password2(self):
        """
                Walidacja potwierdzenia hasła.
                Zwraca:
                - password2: Potwierdzenie hasła, jeśli walidacja przebiegła pomyślnie.
                Wyjątek:
                - forms.ValidationError: Jeśli hasła nie są zgodne.
                """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie pasują do siebie")
        return password2

    # Zapis użytkownika z ustawieniem hasła
    def save(self, commit=True):
        """
                Zapisuje użytkownika do bazy danych z ustawieniem hasła.
                Argumenty:
                - commit: Określa, czy zapisać użytkownika od razu do bazy danych.
                Zwraca:
                - Obiekt User: Zwraca zapisanego użytkownika.
                """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Formularz zmiany danych użytkownika
class UserChangeForm(forms.ModelForm):
    """
        Formularz służący do zmiany danych istniejącego użytkownika.
        Pola:
        - email: Adres email użytkownika.
        - firstname: Imię użytkownika.
        - lastname: Nazwisko użytkownika.
        - phone: Numer telefonu użytkownika.
        - password: Pole do wyświetlania zaszyfrowanego hasła (tylko do odczytu).
        - is_active: Określa, czy użytkownik jest aktywny.
        - is_admin: Określa, czy użytkownik ma uprawnienia administracyjne.
        Metody:
        - clean_password: Metoda czyszcząca pole hasła, zwraca wartość początkową hasła.
        """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'phone', 'password', 'is_active', 'is_admin')

    # Metoda czyszcząca pole hasła (hash)
    def clean_password(self):
        """
               Metoda czyszcząca pole hasła (hash).
               Zwraca:
               - initial["password"]: Zwraca początkową wartość hasła.
               """
        return self.initial["password"]

