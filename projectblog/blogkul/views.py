from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Publication, Like, Comment
from .forms import PublicationForm, CommentForm
from django.contrib.auth.decorators import login_required


def blogkulinarny(request):
    query = request.GET.get('q')
    if query:
        publications = Publication.objects.filter(
            Q(name__icontains=query) |
            Q(author__firstname__icontains=query) |
            Q(author__lastname__icontains=query)
        )
    else:
        publications = Publication.objects.all()

    user = request.user
    for publication in publications:
        publication.liked_by_current_user = publication.like_set.filter(user=user).exists()
        publication.like_count = publication.like_set.count()
        publication.comments = publication.comment_set.all()

    context = {
        'publications': publications,
        'query': query,
    }
    return render(request, 'blogkul.html', context)


@login_required
def add_like(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    Like.objects.get_or_create(user=request.user, publication=publication)
    return redirect('blogkulinarny')


@login_required
def remove_like(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    Like.objects.filter(user=request.user, publication=publication).delete()
    return redirect('blogkulinarny')


@login_required
def add_comment(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publication = publication
            comment.user = request.user
            comment.save()
    return redirect('blogkulinarny')


@login_required
def add_publication(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.author = request.user
            publication.save()
            return redirect('blogkulinarny')
    else:
        form = PublicationForm()
    return render(request, 'blog/add_publication.html', {'form': form})


def publication_detail(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    publication.liked_by_current_user = publication.like_set.filter(user=request.user).exists()
    publication.like_count = publication.like_set.count()
    publication.comments = publication.comment_set.all()

    return render(request, 'blog/publication_detail.html', {'publication': publication})
