from django import forms
from .models import Category, Frontman


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок")
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 label="Категории", empty_label="Категория не выбрана")
    frontman = forms.ModelChoiceField(queryset=Frontman.objects.all(), required=False,
                                      label="Лидер группы", empty_label="Без лидера")
