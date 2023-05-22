from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import *
from .forms import ReviewForm
from django.db.models import Q


class GenreYear:

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    template_name = 'movies_temp/movies_list.html'
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 5


class MovieDetailView(GenreYear, DetailView):
    template_name = 'movies_temp/movie_detail.html'
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = 'url'


class AddReview(View):

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies_temp/actor_detail.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    paginate_by = 2
    template_name = 'movies_temp/movies_list.html'

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class Search(ListView):
    paginate_by = 3
    template_name = 'movies_temp/movies_list.html'

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
