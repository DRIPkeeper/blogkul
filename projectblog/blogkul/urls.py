from django.urls import path, include
from .views import blogkulinarny, add_like, remove_like, add_comment, add_publication, publication_detail
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', blogkulinarny, name='blogkulinarny'),
    path('add_like/<int:publication_id>/', add_like, name='add_like'),
    path('remove_like/<int:publication_id>/', remove_like, name='remove_like'),
    path('add_comment/<int:publication_id>/', add_comment, name='add_comment'),
    path('add_publication/', add_publication, name='add_publication'),
    path('publication/<int:publication_id>/', publication_detail, name='publication_detail'),
    path('strona_glowna', include('stronagl.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
