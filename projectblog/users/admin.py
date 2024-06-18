from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User
from .forms import UserCreationForm, UserChangeForm

# Konfiguracja panelu administracyjnego dla modelu User
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    # Pola wyświetlane w widoku listy użytkowników
    list_display = ('email', 'firstname', 'lastname', 'phone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'phone')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'firstname', 'lastname', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = () # Brak pól do filtrowania w poziomie

admin.site.register(User, UserAdmin) # Rejestracja modelu User i jego konfiguracji w panelu administracyjnym
admin.site.unregister(Group) # Wyrejestrowanie modelu Group, ponieważ nie jest używany
