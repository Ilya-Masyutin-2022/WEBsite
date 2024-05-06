from django import forms
from .models import Category, Frontman


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea())
    is_published = forms.BooleanField()
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
    frontman = forms.ModelChoiceField(queryset=Frontman.objects.all())
