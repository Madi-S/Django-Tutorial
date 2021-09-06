from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from .utils import MyMixin
from .forms import NewsForm
from .models import Category, News


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been registered successfully')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed')
    else:
        form = UserCreationForm()
    return render(request, 'news/register.html', context={'form': form})


def login(request):
    return render(request, 'news/login.html')


def test(request):
    objects = ['John1', 'Madi2', 'Jack3', 'Denmo4', 'John5', 'Madi6', 'Jack7']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    # page_objects = paginator.page(page_num) # throws exception if page does not exist
    return render(request, 'news/test.html', {'page_obj': page_objects})


class HomeNews(MyMixin, ListView):
    model = News
    paginate_by = 2
    mixin_prop = 'hello world'
    context_object_name = 'news'
    # extra_context = {'title': 'Home'}

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home Page'
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    paginate_by = 2
    allow_empty = False
    context_object_name = 'news'
    template_name = 'news/home_news_list.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        category = Category.objects.get(pk=self.kwargs['category_id'])
        context['title'] = category.title
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True, category=self.kwargs['category_id']).select_related('category')


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    template_name = 'news/add_news.html'
    # raise_exception = True


class DetailNews(DetailView):
    model = News

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        news_item = News.objects.get(pk=self.kwargs['pk'])
        context['title'] = news_item.title
        return context


def _index(request):
    news = News.objects.filter(is_published=True).all()
    context = {
        'news': news,
        'title': 'Home'
    }
    return render(request, 'news/index.html', context)


def _view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    context = {
        'news_item': news_item,
        'title': news_item.title
    }
    return render(request, 'news/view_news.html', context)


def _get_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    news = News.objects.filter(category_id=category_id).all()
    context = {
        'news': news,
        'title': category.title,
        'category': category
    }
    return render(request, 'news/category.html', context)


def _add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            print('Form cleaned data:', form.cleaned_data)
            # news = News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    context = {'form': form}
    return render(request, 'news/add_news.html', context)
