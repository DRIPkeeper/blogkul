from django import forms
from .models import Comment
from .models import Publication
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['name', 'content', 'image', 'is_private', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
