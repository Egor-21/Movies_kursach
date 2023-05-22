from django import template

from movies_library.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('movies_temp/tags/last_add_movies.html')
def get_last_add_movies(count=5):
    movies = Movie.objects.order_by("-id")[:count]
    return {"last_movies": movies}