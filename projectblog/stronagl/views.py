from django.shortcuts import render

def strona_glowna(request):
    context = {
        'tytul': 'Witamy na naszej stronie głównej!!!!',
    }
    return render(request, 'stronaglowna.html', context)


