from django.contrib import admin
from .models import Publication, Like, Comment
from django.utils.html import mark_safe

# Rejestracja modelu Publication w panelu admina
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pdate', 'is_private', 'image_tag')
    search_fields = ('name', 'content', 'author__firstname', 'author__lastname')
    list_filter = ('pdate', 'is_private')
    readonly_fields = ('image_tag',)
    fields = ('name', 'author', 'content', 'image', 'is_private', 'password', 'pdate', 'image_tag')

    # Metoda do wyświetlania obrazu w adminie
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return '-'
    image_tag.short_description = 'Image'

# Rejestracja modelu Like w panelu admina
class LikeAdmin(admin.ModelAdmin):
    list_display = ('publication_name', 'user', 'created_at')
    search_fields = ('publication__name', 'user__email')
    list_filter = ('created_at',)

    # Metoda do wyświetlania nazwy publikacji
    def publication_name(self, obj):
        return obj.publication.name
    publication_name.admin_order_field = 'publication'
    publication_name.short_description = 'Publication'

# Rejestracja modelu Comment w panelu admina
class CommentAdmin(admin.ModelAdmin):
    list_display = ('publication_name', 'user', 'text', 'cdate')
    search_fields = ('publication__name', 'user__email', 'text')
    list_filter = ('cdate',)

    # Metoda do wyświetlania nazwy publikacji
    def publication_name(self, obj):
        return obj.publication.name
    publication_name.admin_order_field = 'publication'
    publication_name.short_description = 'Publication'

# Rejestracja modeli w panelu admina
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
