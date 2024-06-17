from django.urls import path
from .views import strona_glowna

urlpatterns = [
    path('', strona_glowna, name='strona_glowna'),

]
