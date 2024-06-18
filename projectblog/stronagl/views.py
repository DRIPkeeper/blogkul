from django.shortcuts import render

def strona_glowna(request):
    """
        Widok odpowiedzialny za renderowanie strony głównej aplikacji.
        Argumenty:
        - request: Obiekt HttpRequest reprezentujący żądanie HTTP.
        Zwraca:
        - HttpResponse: Renderuje szablon 'stronaglowna.html' z przekazanym kontekstem,
          zawierającym tytuł strony głównej.
        Kontekst:
        - 'tytul': Tytuł wyświetlany na stronie głównej.
        """
    context = {
        'tytul': 'Witamy na naszej stronie głównej!!!!',
    }
    return render(request, 'stronaglowna.html', context)


