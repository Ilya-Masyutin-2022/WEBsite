from django import template
import bands.views as views
from bands.models import Category

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories():
    return views.cats_db


@register.inclusion_tag('bands/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected_id}



