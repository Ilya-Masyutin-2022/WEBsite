from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from bands.forms import AddPostForm
from bands.models import Bands, Category, TagPost

from bands.utils import DataMixin

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


class ShowPost(DataMixin, DetailView):
    model = Bands
    template_name = 'bands/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'])


class TagPostList(DataMixin, ListView):
    template_name = 'bands/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title='Тег: ' + tag.tag)


def get_queryset(self):
    return Bands.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class BandsHome(DataMixin, ListView):
    template_name = 'bands/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Bands.published.all().select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница',
                                      cat_selected=0)


class BandsCategory(DataMixin, ListView):
    template_name = 'bands/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id)

    def get_queryset(self):
        return Bands.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


def about(request):
    contact_list = Bands.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bands/about.html',
                  {'page_obj': page_obj, 'title': 'О сайте'})


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
    title_page = 'Добавление статьи'


class UpdatePage(UpdateView):
    model = Bands
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'bands/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


class DeletePage(DeleteView):
    model = Bands
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'bands/deletepage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
