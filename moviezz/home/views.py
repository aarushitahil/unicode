import requests
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import MoviesSearched

apikey = 'c2ab0e02'
url = 'http://www.omdbapi.com/'

class InputGenre(forms.Form):
    title = forms.CharField(label='Title Prompt:', max_length=100)
    genre = forms.CharField(label='Genre(Optional):', max_length=30, required=False)

def home(request):
    if request.method == 'POST':        #why are we doing this
        form = InputGenre(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            genre = form.cleaned_data['genre']

            if genre:
                response = requests.get(f'{url}?s={title}&apikey={apikey}&page=1')
                all = response.json().get('Search', [])
                finalmovies = []
                for movie in all:
                    movie_details = requests.get(f'{url}?i={movie["imdbID"]}&apikey={apikey}').json()
                    if genre.lower() in movie_details['Genre'].lower():
                        finalmovies.append(movie)
            else:
                response = requests.get(f'{url}?s={title}&apikey={apikey}&page=1')
                finalmovies = response.json().get('Search', [])

            if finalmovies:
                    first_movie = finalmovies[0]
                    movie_details = requests.get(f'{url}?i={first_movie["imdbID"]}&apikey={apikey}').json()
                    movie, created = MoviesSearched.objects.get_or_create(
                        title=movie_details.get('Title'), 
                        released=movie_details.get('Released'), defaults = {        #only title and release date are used to search
                        'runtime': movie_details.get('Runtime'),                    #defaults is only fetched if object is being created
                        'imdb_rating': movie_details.get('imdbRating')
                        })
                    if not created:
                        movie.count += 1
                        movie.save()

                    return search_results(request, finalmovies=finalmovies)
            else:
                return HttpResponse('<body>No matches found.</body>')
    else:
        form = InputGenre()
    return render(request, 'home.html', {'form': form})

def search_results(request, finalmovies):
    return render(request, 'search_results.html', {'movies': finalmovies})

def movie_details(request, title):
    response = requests.get(f'{url}?t={title}&apikey={apikey}')
    movie = response.json()
    return render(request, 'movie_details.html', {'movie': movie})

def previously_searched(request):
    movies = MoviesSearched.objects.all()
    return render(request, 'previously_searched.html', {'movies': movies})
