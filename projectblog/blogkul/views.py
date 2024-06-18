from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Publication, Like, Comment
from .forms import PublicationForm, CommentForm
from django.contrib.auth.decorators import login_required

# Widok głównej strony bloga
def blogkulinarny(request):
    """
       Widok odpowiedzialny za wyświetlanie głównej strony bloga.
       Argumenty:
       - request: Obiekt HttpRequest reprezentujący żądanie HTTP.
       Zwraca:
       - HttpResponse: Renderuje szablon 'blogkul.html' z kontekstem zawierającym listę
         publikacji oraz zapytanie wyszukiwania.

       """
    query = request.GET.get('q')  # Pobranie zapytania wyszukiwania
    if query:
        # Filtracja publikacji na podstawie zapytania
        publications = Publication.objects.filter(
            Q(name__icontains=query) |
            Q(author__firstname__icontains=query) |
            Q(author__lastname__icontains=query)
        )
    else:
        # Pobranie wszystkich publikacji
        publications = Publication.objects.all()

    user = request.user  # Pobranie aktualnego użytkownika
    for publication in publications:
        # Sprawdzenie, czy użytkownik polubił publikację
        publication.liked_by_current_user = publication.like_set.filter(user=user).exists()
        # Zliczanie polubień publikacji
        publication.like_count = publication.like_set.count()
        # Pobranie wszystkich komentarzy do publikacji
        publication.comments = publication.comment_set.all()

    context = {
        'publications': publications,
        'query': query,
    }
    return render(request, 'blogkul.html', context)

# Widok dodawania polubienia do publikacji
@login_required
def add_like(request, publication_id):
    """
        Widok odpowiedzialny za dodawanie polubienia do wybranej publikacji.
        Argumenty:
        - request: Obiekt HttpRequest reprezentujący żądanie HTTP.
        - publication_id: Identyfikator publikacji, do której dodawane jest polubienie.
        Zwraca:
        - HttpResponse: Przekierowanie na stronę główną bloga ('blogkulinarny') po dodaniu polubienia.
        """
    publication = get_object_or_404(Publication, id=publication_id)
    Like.objects.get_or_create(user=request.user, publication=publication)
    return redirect('blogkulinarny')

# Widok usuwania polubienia z publikacji
@login_required
def remove_like(request, publication_id):
    """
        Widok odpowiedzialny za usuwanie polubienia z wybranej publikacji.
        Argumenty:
        - request: Obiekt HttpRequest reprezentujący żądanie HTTP.
        - publication_id: Identyfikator publikacji, z której usuwane jest polubienie.
        Zwraca:
        - HttpResponse: Przekierowanie na stronę główną bloga ('blogkulinarny') po usunięciu polubienia.
        """
    publication = get_object_or_404(Publication, id=publication_id)
    Like.objects.filter(user=request.user, publication=publication).delete()
    return redirect('blogkulinarny')

# Widok dodawania komentarza do publikacji
@login_required
def add_comment(request, publication_id):
    """
        Widok odpowiedzialny za dodawanie komentarza do wybranej publikacji.
        Argumenty:
        - request: Obiekt HttpRequest reprezentujący żądanie HTTP.
        - publication_id: Identyfikator publikacji, do której dodawany jest komentarz.
        Zwraca:
        - HttpResponse: Przekierowanie na stronę główną bloga ('blogkulinarny') po dodaniu komentarza.
        """
    publication = get_object_or_404(Publication, id=publication_id)  # Pobranie publikacji
    if request.method == 'POST':
        form = CommentForm(request.POST)  # Utworzenie formularza komentarza
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publication = publication
            comment.user = request.user
            comment.save()  # Zapisanie komentarza
    return redirect('blogkulinarny')

# Widok dodawania nowej publikacji
@login_required
def add_publication(request):
    """
        Widok odpowiedzialny za dodawanie nowej publikacji.
        Argumenty:
        - request: Obiekt HttpRequest reprezentujący żądanie HTTP.
        Zwraca:
        - HttpResponse: Renderuje szablon 'blog/add_publication.html' z formularzem do dodawania publikacji
          lub przekierowuje na stronę główną bloga ('blogkulinarny') po zapisaniu nowej publikacji.

        """
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)  # Utworzenie formularza publikacji
        if form.is_valid():
            publication = form.save(commit=False)
            publication.author = request.user
            publication.save()  # Zapisanie publikacji
            return redirect('blogkulinarny')
    else:
        form = PublicationForm()  # Utworzenie pustego formularza publikacji
    return render(request, 'blog/add_publication.html', {'form': form})

# Widok szczegółów publikacji
def publication_detail(request, publication_id):
    """
       Widok odpowiedzialny za wyświetlanie szczegółów wybranej publikacji.
       Argumenty:
       - request: Obiekt HttpRequest reprezentujący żądanie HTTP.
       - publication_id: Identyfikator publikacji, której szczegóły są wyświetlane.
       Zwraca:
       - HttpResponse: Renderuje szablon 'blog/publication_detail.html' z danymi wybranej publikacji
         oraz informacjami o liczbie polubień i listą komentarzy.
       """
    publication = get_object_or_404(Publication, id=publication_id)
    publication.liked_by_current_user = publication.like_set.filter(user=request.user).exists()
    publication.like_count = publication.like_set.count()
    publication.comments = publication.comment_set.all()

    return render(request, 'blog/publication_detail.html', {'publication': publication})
