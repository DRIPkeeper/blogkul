from django import forms
from .models import Comment
from .models import Publication

# Formularz dla modelu Comment
class CommentForm(forms.ModelForm):
    """
        Klasa formularza do obsługi danych modelu Comment.
        Pola:
        - text: Tekst komentarza.
        Użycie:
        Tworzenie instancji tego formularza służy do tworzenia lub aktualizowania komentarzy
        powiązanych z obiektem Publication. Formularz zapewnia walidację danych i umożliwia interakcję
        z modelem Comment w Django.
        Przykład:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publication = <instancja Publication>
            comment.user = request.user
            comment.save()

        """
    class Meta:
        model = Comment
        fields = ['text']

# Formularz dla modelu Publication
class PublicationForm(forms.ModelForm):
    """
        Klasa formularza do obsługi danych modelu Comment.
        Pola:
        - text: Tekst komentarza.
        Użycie:
        Tworzenie instancji tego formularza służy do tworzenia lub aktualizowania komentarzy
        powiązanych z obiektem Publication. Formularz zapewnia walidację danych i umożliwia interakcję
        z modelem Comment w Django.
        Przykład:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publication = <instancja Publication>
            comment.user = request.user
            comment.save()
        """
    class Meta:
        model = Publication
        fields = ['name', 'content', 'image', 'is_private', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
