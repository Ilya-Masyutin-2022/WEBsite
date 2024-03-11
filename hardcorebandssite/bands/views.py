from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


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


data_db = [
 {'id': 1, 'title': 'Motionless In White', 'content':
     '''Motionless in White — американская метал-группа из города Скрентон, штат Пенсильвания. 
     Коллектив был основан в 2004 году и стал известен благодаря мрачным текстам и готическому внешнему виду участников. 
     На данный момент в группе состоят Крис Черулли, Рикки Олсон, Райан Ситковски, Винни Мауро и Джастин Морроу. 
     Сейчас Motionless in White подписаны на Roadrunner Records и выпустили два EP и шесть полноформатных альбомов. 
     Их альбом Creatures достиг 175 позиции в Billboard 200 в 2010 году.
     ''', 'is_published': True},
 {'id': 2, 'title': 'Architects', 'content': 'История', 'is_published': False},
 {'id': 3, 'title': 'Bring Me The Horizon', 'content':
     '''Bring Me the Horizon — британская рок-группа из Шеффилда, Йоркшира, основанная в 2004 году. 
     В настоящее время состоит из вокалиста Оливера Сайкса, гитариста Ли Малии, 
     басиста Мэтта Кина и барабанщика Мэтта Николлса.
     На данный момент группа имеет шесть выпущенных полноформатных альбомов и четыре мини-альбома. 
     На протяжении карьеры участники старались экспериментировать со звучанием: 
     ранние релизы имели более тяжёлый звук и были классифицированы как дэткор и металкор. 
     Позднее в звучание группы добавились элементы мелодичного хардкора, альтернативного, электронного и пост-рока.
     В 2013 году был выпущен альбом «Sempiternal», принесший группе новую волну популярности 
     и открывший ей перспективы выступления на аренах в качестве хэдлайнера. 
     В следующем альбоме That's the Spirit, вышедшем в 2015 году, группа продолжила творческие эксперименты, 
     отказавшись от привычного металкор звучания в пользу альтернативного рока. 
     В 2019 году состоялся релиз альбома Amo, записанный в стиле электронной, поп-рок, альтернативный рок, 
     электропоп и хард-рок. В 2020 году 31 октября вышел в свет EP под названием Post Human: 
     Survival Horror, который является первым из четырех альбомов из серии Post Human''', 'is_published': True},
]


def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'bands/index.html', context=data)


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def index(request):  # HttpRequest
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0,
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


