from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

# Manager użytkowników
class UserManager(BaseUserManager):
    # Tworzenie zwykłego użytkownika
    def create_user(self, email, firstname, lastname, phone, password=None):
        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Tworzenie super użytkownika (administratora)
    def create_superuser(self, email, firstname, lastname, phone, password=None):
        user = self.create_user(
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# Model użytkownika
class User(AbstractBaseUser):
    id = models.CharField(max_length=200, default=uuid.uuid4, unique=True, primary_key=True)  # Unikalny identyfikator użytkownika
    email = models.EmailField(null=False, max_length=100, unique=True)  # Adres email użytkownika
    firstname = models.CharField(null=False, max_length=100)
    lastname = models.CharField(null=False, max_length=100)
    phone = models.IntegerField(null=False, unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)  # Czy użytkownik jest administratorem
    is_active = models.BooleanField(default=True)  # Czy użytkownik jest aktywny
    is_staff = models.BooleanField(default=False)  # Czy użytkownik jest członkiem personelu
    is_superuser = models.BooleanField(default=False)  # Czy użytkownik jest super użytkownikiem

    USERNAME_FIELD = 'email'  # Pole używane do logowania (email)
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phone']  # Wymagane pola do tworzenia użytkownika

    objects = UserManager()  # Obiekt managera użytkowników

    def __str__(self):
        return self.email + ", " + self.firstname  # Zwraca reprezentację tekstową użytkownika

    # Metoda sprawdzająca uprawnienia użytkownika
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Metoda sprawdzająca uprawnienia użytkownika w module
    def has_module_perms(self, app_label):
        return True
