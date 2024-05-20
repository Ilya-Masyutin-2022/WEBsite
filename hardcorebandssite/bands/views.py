from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView, CreateView
from django.views.generic import ListView

from bands.forms import AddPostForm, UploadFileForm
from bands.models import Bands, Category, TagPost, UploadFiles

import uuid

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


class ShowPost(DetailView):
    model = Bands
    template_name = 'bands/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Bands.published, slug=self.kwargs[self.slug_url_kwarg])


class TagPostList(ListView):
    template_name = 'bands/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context

    def get_queryset(self):
        return Bands.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class BandsHome(ListView):
    template_name = 'bands/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Bands.published.all().select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['cat_selected'] = 0
        return context


class BandsCategory(ListView):
    template_name = 'bands/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.id
        return context

    def get_queryset(self):
        return Bands.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'bands/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    return render(request, 'bands/addpage.html',
                  {'menu': menu, 'title': 'Добавление статьи', 'form': form})


class AddPage(CreateView):
    model = Bands
    fields = ['title', 'slug', 'content', 'is_published', 'cat']
    template_name = 'bands/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
