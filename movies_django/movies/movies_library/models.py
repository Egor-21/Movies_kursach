from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Модель категорий фильмов"""
    title = models.CharField("Категория", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    """Модель жанров фильма"""
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Actor(models.Model):
    """Модель актёров и режиссёров"""
    name = models.CharField("Имя", max_length=200)
    description = models.TextField("Описание")
    birth_date = models.DateField("Дата рождения", default=date.today)
    photo = models.ImageField("Фото", upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Актёры и режиссёры"
        verbose_name_plural = "Актёры и режиссёры"


class Movie(models.Model):
    """Модель фильмов"""
    title = models.CharField("Название", max_length=200)
    slogan = models.CharField("Слоган", max_length=200, default="")
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to='movies/')
    country = models.CharField("Страна", max_length=200)
    year = models.IntegerField("Год выхода", default=2023)
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    directors = models.ManyToManyField(Actor, verbose_name="режиссёр", related_name='movie_director')
    actors = models.ManyToManyField(Actor, verbose_name="актёры", related_name='movie_actor')
    date = models.DateField("Дата выхода", default=date.today)
    budget = models.IntegerField("Бюджет фильма", default=0)
    fees = models.IntegerField("Сборы", default=0)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=200, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShot(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    shot = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class Review(models.Model):
    name = models.CharField("Имя", max_length=200)
    email = models.EmailField()
    text = models.TextField("Сообщение", max_length=10000)
    parent = models.ForeignKey('self', verbose_name='Родитель',on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"