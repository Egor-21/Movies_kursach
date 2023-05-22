from django.contrib import admin
from .models import *
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "url"]
    list_display_links = ['title']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url', 'draft']
    list_filter = ['category', 'year']
    save_on_top = True
    save_as = True
    search_fields = ['title', 'category__title']
    form = MovieAdminForm
    actions = ['publish', 'unpublish']

    fieldsets = (
        ('Title', {
            "fields": (('title', 'slogan'),)
        }),
        ('Description', {
            "fields": ('description', ('poster',))
        }),
        ('Year', {
            "fields": (('year', 'country', 'date'),)
        }),
        ('Actors', {
            'classes': ['collapse'],
            'fields': (('actors', 'directors'), ('genres', 'category'),)
        }),
        ('Fees', {
            'fields': (('budget', 'fees'),)
        }),
        (None, {
            'fields': (('url', 'draft'),)
        }),


    )

    # def get_image(self, obj):
    #     return mark_safe(f'<img src={obj.poster.url} width="150" hight = "160"')

    # def unpublish(self, request, queryset):
    #     row_update = queryset.update(draft=True)
    #     message_bit = f"{row_update} записей были обновлены"
    #     self.message_user(request, f'{message_bit}')
    #
    # def publish(self, request, queryset):
    #     row_update = queryset.update(draft=False)
    #     message_bit = f"{row_update} записей были обновлены"
    #     self.message_user(request, f'{message_bit}')
    #
    # publish.short_description = 'Опубликовать'
    # publish.allowed_permissions = ['change']
    #
    # unpublish.short_description = 'Убрать публикацию'
    # publish.allowed_permissions = ['change']
    #
    # get_image.short_description = 'Постер'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'get_image']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="150" hight = "160"')

    get_image.short_description = 'Изображение'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'parent', 'movie', 'id']
    readonly_fields = ['name', 'email']


@admin.register(MovieShot)
class MovieShotAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie', 'get_image']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.shot.url} width="150" hight = "160"')


admin.site.site_title = "Movies Library"
admin.site.site_header = "Movies Library"