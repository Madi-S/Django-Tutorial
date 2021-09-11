from django.urls import path

from .views import HomeNews, NewsByCategory, DetailNews, CreateNews, user_register, user_login, user_logout, contacts


urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('news/<int:pk>/', DetailNews.as_view(), name='view_news'),
    path('category/<int:category_id>/',
         NewsByCategory.as_view(), name='category'),
]
