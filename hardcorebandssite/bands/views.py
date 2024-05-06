from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from bands.models import Bands, Category, TagPost

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'addpage'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]


cats_db = [
 {'id': 1, 'name': 'Металкор'},
 {'id': 2, 'name': 'Дэткор'},
 {'id': 3, 'name': 'Пост-хардкор'},
]


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Bands.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'bands/index.html', context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Bands, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'bands/post.html',
                  context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Bands.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'bands/index.html', context=data)


def index(request):  # HttpRequest
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Bands.published.all(),
        'cat_selected': 0,
    }
    return render(request, 'bands/index.html', context=data)


def about(request):
    return render(request, 'bands/about.html',
                  {'title': 'О сайте', 'menu': menu})


def addpage(request):
    return render(request, 'bands/addpage.html',
                  {'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


