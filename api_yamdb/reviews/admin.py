from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    """Администрирование категорий произведений."""

    list_display = ('name', 'slug',)
    list_editable = ('slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    list_display_links = ('name',)[:10]


class CommentAdmin(admin.ModelAdmin):
    """Администрирование комментариев произведения."""

    list_display = ('author', 'review', 'text', 'pub_date')
    list_editable = ('author', 'review',)
    search_fields = ('author', 'text',)
    list_display_links = ('text',)[:10]


class GenreAdmin(admin.ModelAdmin):
    """Администрирование жанров произведений."""

    list_display = ('name', 'slug',)
    list_editable = ('slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    list_display_links = ('name',)[:10]


class ReviewAdmin(admin.ModelAdmin):
    """Администрированеи отзывов произведений."""

    list_display = ('author', 'title', 'text', 'score', 'pub_date')
    list_editable = ('author', 'text', 'score',)
    search_fields = ('author', 'title', 'text', 'score',)
    list_display_links = ('title',)[:10]


class TitleAdmin(admin.ModelAdmin):
    """Администрирование произведений."""

    list_display = (
        'name', 'description', 'year', 'category',)
    list_editable = ('description', 'year', 'category',)
    search_fields = ('name', 'genre', 'category',)
    list_display_links = ('name',)[:10]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
