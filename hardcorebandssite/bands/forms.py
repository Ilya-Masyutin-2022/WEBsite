from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Frontman, Bands
from django.core.validators import MinLengthValidator, MaxLengthValidator


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Изображение")


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label="Категория не выбрана", label="Категории")
    frontman = forms.ModelChoiceField(queryset=Frontman.objects.all(),
                                      required=False, empty_label="Без лидера", label="Лидер группы")

    class Meta:
        model = Bands
        fields = ['title', 'slug', 'content', 'photo',
                  'is_published', 'cat', 'frontman', 'tags']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

    title = forms.CharField(max_length=255,
                            min_length=5, label="Заголовок",
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                'min_length': 'Слишком короткий заголовок',
                                'required': 'Без заголовка - никак',
                            })

    slug = forms.SlugField(max_length=255, label="URL",
                           validators=[MinLengthValidator(5, message="Минимум 5 символов"),
                                       MaxLengthValidator(100, message="Максимум 100 символов")])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)