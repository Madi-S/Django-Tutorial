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
