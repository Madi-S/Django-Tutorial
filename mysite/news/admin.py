from django.contrib import admin

from .models import News, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_published',
                    'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('category', 'is_published')
    list_filter = ('is_published', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
