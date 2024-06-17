from django.contrib import admin
from .models import Publication, Like, Comment
from django.utils.html import mark_safe

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pdate', 'is_private', 'image_tag')  # Добавление автора и приватности
    search_fields = ('name', 'content', 'author__firstname', 'author__lastname')  # Добавление поиска по автору
    list_filter = ('pdate', 'is_private')  # Фильтр по приватности
    readonly_fields = ('image_tag',)  # Поле только для чтения в админке
    fields = ('name', 'author', 'content', 'image', 'is_private', 'password', 'pdate', 'image_tag')  # Указание полей для редактирования

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return '-'
    image_tag.short_description = 'Image'

class LikeAdmin(admin.ModelAdmin):
    list_display = ('publication_name', 'user', 'created_at')
    search_fields = ('publication__name', 'user__email')
    list_filter = ('created_at',)

    def publication_name(self, obj):
        return obj.publication.name
    publication_name.admin_order_field = 'publication'
    publication_name.short_description = 'Publication'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('publication_name', 'user', 'text', 'cdate')
    search_fields = ('publication__name', 'user__email', 'text')
    list_filter = ('cdate',)

    def publication_name(self, obj):
        return obj.publication.name
    publication_name.admin_order_field = 'publication'
    publication_name.short_description = 'Publication'

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
