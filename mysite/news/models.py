from django.db import models
from django.urls import reverse, reverse_lazy


'''
primary_key id is created by default
nullable=false (by default all fields are not nullable)
auto_now_add - set current date on creation
auto_now - set current date on modify
upload_to - directory: str to store images or method to handle it
'''


class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Publishing date')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Updating date')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    is_published = models.BooleanField(
        default=True, verbose_name='Published status')
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, related_name='news')
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'News {self.id}: {self.title}'

    def get_absolute_url(self):
        return reverse_lazy('view_news', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'News Item'
        verbose_name_plural = 'News Items'
        ordering = ['-created_at', 'title']


class Category(models.Model):
    title = models.CharField(
        max_length=100, db_index=True, verbose_name='Catrgory name')
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']


'''
RAW SQL
>>> news = News.objects.raw('SELECT * FROM news_news')
>>> for item in news:
>>>     print(item)

>>> news = News.objects.raw('SELECT id, title FROM news_news')
all raw queries must inlcude primary key field

>>> news[0].content
django can query any fields that are not included in the query string
but this is not efficient and not recommended

>>> news = News.objects.raw('SELECT * FROM news_news WHERE title = %s', ('My Title',))
anti sql-injections query


SQL FUNCTIONS (RECOMMENDED), CALCULATE TITLE LENGTH:
>>> from django.db.models.functions import Length
>>> news = News.objects.annotate(length=Length('title')).first()
>>> news.length


FILTER NEWS, WHICH HAVE TITLE IN THEIR CONTENT (INNER FIELDS REFERENCE):
>>> News.objects.filter(content__icontains=F('title'))


INCREMENT VIEWS COUNT FOR NEWS:
>>> from django.db.models import F
>>> news1 = News.objects.first()
>>> news1.views = F('views') + 1
>>> news1.save()


VALUES (QUERY ONLY NEEDED FIELDS):
>>> news3 = News.objects.values('title', 'views').get(pk=3)
returns a dictionary with given fields
>>> news3['title']      -   'Title modified 3'
>>> news3['category']   -   error

>>> news = News.objects.values('title', 'views', 'category__title')


ANNOTATIONS:
Get news count for categories
>>> cats = Category.objects.annotate(news_count=Count('news'))
>>> cats[0].news_count
7

Get max views for categories
>>> cats = Category.objects.annotate(max_views=Max('news__views'))
>>> cats[2].max_views
1000

Get total count/sum of views for categories 
>>> cats = Category.objects.annotate(sum_views=Sum('news__views'))
>>> cats[2].sum_views
1000

Get categories, which have more than 1 news
>>> cats = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=1).all()
Culture 7
Politics 4
Science 5

Get count of news with unique views count
>>> News.objects.aggregate(cnt=Count('views', distinct=True))
{'cnt': 2}


AGGREGATORS:
>>> from django.db.models import *
>>> News.objects.aggregate(Min('views'), Max('views'))
{'views__min': 0, 'views__max': 1000}

>>> News.objects.aggregate(min_views=Min('views'), max_views=Max('views'))
{'min_views': 0, 'max_views': 1000}

>>> News.objects.aggregate(diff=Min('views')-Max('views'))
{'diff': -1000}

>>> News.objects.aggregate(Sum('views'))
{'views__sum': 1000}

>>> News.objects.aggregate(Avg('views'))
{'views__avg': 62.5}


LOOKUPS / CONDITIONS:
All lookups are formed like: <column_name>__<condition_name>
All filters can be chained .filter(pk_in=(1,2,3), title__contains='Title', ...)

>>> Category.objects.filter(pk__gt=2).all()   -  WHERE id > 2
>>> Category.objects.filter(pk__gte=2).all()  -  WHERE id >= 2
>>> Category.objects.filter(pk__lt=2).all()   -  WHERE id < 2
>>> Category.objects.filter(pk__lte=2).all()  -  WHERE id <= 2

>>> Category.objects.filter(title__contains='s').all()  - case sensitive
>>> Category.objects.filter(title__icontains='s').all() - case insensitive

>>> Category.objects.filter(pk__in=(1,2,3)).all()

>>> Category.objects.first()
>>> Category.objects.last()

>>> Category.objects.earliest('created_at')
>>> Category.objects.latest('updated_at')

>>> Category.objects.filter(...).exists()   - returns boolean
>>> Category.objects.filter(...).count()    - returns number
>>> Category.objects.filter(...).distinct() - returns unique objects

>>> news6.get_next_by_created_at()        - returns next news with id=6
>>> news6.get_previous_by_created_at()    - returns previous news with id=4
>>> news6.get_previous_by_created_at(pk__gt=4)    - also takes lookups as arguments
get_next_<datetime_field_name>()
get_previous_<datetime_field_name>()

>>> News.objects.filter(category__title='Politics').all()
>>> News.objects.filter(category__title__contains='s').all()


LOGICAL OPERATORS:
>>> from django.db.models import Q
>>> News.objects.filter(Q(pk__in=[7,9]) | Q(title__contains='admin')).all()     - OR
>>> News.objects.filter(Q(pk__in=[7,9]) & ~Q(title__contains='admin')).all()    - NOT


RELATIONSHIPS:
>>> cat4 = Category.objects.get(pk=4)
>>> cat4.news_set.all().reverse() 
news_set can be renamed in `related_name` argument for ForeignKey


DELETE objects:
>>> news_5 = News.objects.get(pk=5)
>>> news_5.delete()
(1, {'news.News': 1})


UPDATE objects:
>>> news_3 = News.objects.get(pk=3)
>>> news_3.title = 'Title modified 3'
>>> news_3.save()


QUERY objects:
>>> News.objects.all()
>>> News.objects.filter(title='Title 4')

>>> News.objects.get(pk=5)
or specify any other unique field

>>> News.objects.get(title='Title 5')
raises exception when 0 or > 1 records

>>> News.objects.order_by('title')  ASC
>>> News.objects.order_by('-title') DESC

>>> News.objects.exclude(title='Title 4')
get all objects except for


CREATE db objects:
>>> obj = News(title='Title', content='Some content', ...)
>>> obj.save()

or
>>> obj = News()
>>> obj.title = 'Title 3'
>>> obj.content = 'Content 3'
>>> obj.save()

or without saving
>>> obj = News.objects.create(title='Title 4', content='Content 4')


LAST queries history:
>>> from django.db import connection
>>> connection.queries


MIGRATIONS:
1)  python manage.py makemigrations (optionally specify project name: news)
2) python manage.py sqlmigrate news 0001 (see the sql query, 0001 is the id of migration, news is the project name)
3) python manage.py migrate (run the migration)
'''
