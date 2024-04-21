from django.contrib import admin, messages
from .models import Bands, Category


@admin.register(Bands)
class BandsAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title', )
    list_editable = ('is_published', )
    ordering = ['-time_create', 'title']
    list_per_page = 3
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']

    @admin.display(description="Краткое описание")
    def brief_info(self, bands: Bands):
        return f"Описание {len(bands.content)} символов."

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

