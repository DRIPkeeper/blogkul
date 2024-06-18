from django.conf import settings
from django.db import models
from django.utils import timezone
from PIL import Image
import os
from users.models import User

# Model dla publikacji
class Publication(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    pdate = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='publication_images/', default='publication_images/def.png')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=255, blank=True, null=True)

    # Metoda zapisu publikacji
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Przeskalowanie obrazu do 500x500 pikseli
        if self.image:
            img_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            with Image.open(img_path) as img:
                if img.size != (500, 500):
                    img = img.resize((500, 500), Image.Resampling.LANCZOS)
                    img.save(img_path)
                print(f"Image saved at {img_path} with size {img.size}")

    # Metoda zwracająca liczbę polubień
    def like_count(self):
        return self.like_set.count()

    # Metoda zwracająca nazwę publikacji
    def __str__(self):
        return self.name

# Model dla polubień
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Użytkownik, który polubił
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)  # Polubiona publikacja
    created_at = models.DateTimeField(auto_now_add=True)

    # Metoda zwracająca opis polubienia
    def __str__(self):
        return f"Like by {self.user.firstname} on {self.publication.name}"

# Model dla komentarzy
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Użytkownik, który skomentował
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)  # Skomentowana publikacja
    text = models.TextField()
    cdate = models.DateTimeField(default=timezone.now)

    # Metoda zwracająca opis komentarza
    def __str__(self):
        return f"Comment by {self.user.firstname} on {self.publication.name}"
