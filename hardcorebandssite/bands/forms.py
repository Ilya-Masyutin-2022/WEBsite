from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Frontman
from django.core.validators import MinLengthValidator, MaxLengthValidator


class AddPostForm(forms.Form):
    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789 - "

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские символы, дефис и пробел.")
        return title

    title = forms.CharField(max_length=255,
                            min_length=5, label="Заголовок",
                            widget=forms.TextInput(attrs={'class': 'form - input'}),
                            validators=[clean_title()],
                            error_messages={'min_length': 'Слишком короткий заголовок',
                                            'required': 'Без заголовка - никак'})
    slug = forms.SlugField(max_length=255, label="URL",
                           validators=[MinLengthValidator(5, message="Минимум 5 символов"),
                                       MaxLengthValidator(100, message="Максимум 100 символов")])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 label="Категории", empty_label="Категория не выбрана")
    frontman = forms.ModelChoiceField(queryset=Frontman.objects.all(), required=False, 
                                      label="Лидер группы", empty_label="Без лидера")
        