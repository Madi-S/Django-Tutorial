from django import template
from django.db.models import Count, F

from news.models import Category


register = template.Library()


@register.simple_tag(name='get_categories_list')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Hello', arg2='World'):
    categories = Category.objects \
    .annotate(news_count=Count('news', filter=F('news__is_published'))) \
    .filter(news_count__gt=0).all()
    return {'categories': categories, 'arg1': arg1, 'arg2': arg2}
