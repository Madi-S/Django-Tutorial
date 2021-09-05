from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_published',
                    'created_at', 'updated_at', 'display_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('category', 'is_published')
    list_filter = ('is_published', 'category')
    fields = ('title', 'category', 'content', 'photo', 'display_photo',
              'is_published', 'views', 'created_at', 'updated_at')
    readonly_fields = ('display_photo', 'views', 'created_at', 'updated_at')

    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src={obj.photo.url} width="75px">')
        return 'No photo set'

    display_photo.short_description = 'Current photo'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'News Management'
admin.site.site_header = 'News Management'
