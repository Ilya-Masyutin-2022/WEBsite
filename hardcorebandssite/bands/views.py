from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from bands.models import Bands

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


def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': Bands.published.all(),
        'cat_selected': cat_id,
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


def index(request):  # HttpRequest
    posts = Bands.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'bands/index.html', context=data)


def about(request):
    return render(request, 'bands/about.html',
                  {'title': 'О сайте', 'menu': menu})


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


