from django.urls import path

from .views import HomeNews, NewsByCategory, DetailNews, CreateNews


urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('news/<int:pk>/', DetailNews.as_view(), name='view_news'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
]
