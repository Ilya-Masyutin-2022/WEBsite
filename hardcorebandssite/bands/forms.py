from django import forms
from .models import Category, Frontman
from django.core.validators import MinLengthValidator, MaxLengthValidator


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5, label="Заголовок")
    widget = forms.TextInput(attrs={'class': 'form-input'})
    slug = forms.SlugField(max_length=255, label="URL",
                           validators=[MinLengthValidator(5, message="Минимум 5 символов"),
                                       MaxLengthValidator(100, message="Максимум 100 символов")])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 label="Категории", empty_label="Категория не выбрана")
    frontman = forms.ModelChoiceField(queryset=Frontman.objects.all(), required=False,
                                      label="Лидер группы", empty_label="Без лидера")
