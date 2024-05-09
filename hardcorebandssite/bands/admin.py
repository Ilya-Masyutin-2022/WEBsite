from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Bands, Category


class FrontmanFilter(admin.SimpleListFilter):
    title = 'Лидер группы'
    parameter_name = 'OneFrontman'

    def lookups(self, request, model_admin):
        return [
            ('OneFrontman', 'Есть'),
            ('NoFrontman', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'OneFrontman':
            return queryset.filter(frontman__isnull=False)
        elif self.value() == 'NoFrontman':
            return queryset.filter(frontman__isnull=True)


@admin.register(Bands)
class BandsAdmin(admin.ModelAdmin):
    save_on_top = True
    filter_horizontal = ['tags']
    fields = ['title', 'slug', 'content', 'photo',
              'post_photo', 'cat', 'frontman', 'tags']
    readonly_fields = ['post_photo']
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title', )
    list_editable = ('is_published', )
    ordering = ['-time_create', 'title']
    list_per_page = 3
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [FrontmanFilter, 'cat__name', 'is_published']

    @admin.display(description="Изображение")
    def post_photo(self, bands: Bands):
        if bands.photo:
            return mark_safe(f"<img src = '{bands.photo.url}'width = 50 > ")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Bands.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Bands.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
