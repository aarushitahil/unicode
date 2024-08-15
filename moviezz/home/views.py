import requests
from django.shortcuts import render
from django.http import HttpResponse
from .models import MoviesSearched
from .forms import *

apikey = 'c2ab0e02'
url = 'http://www.omdbapi.com/'


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

def movie_comparison(request):
    if request.method == 'POST':        #why are we doing this
        form = MovieComparison(request.POST)

        if form.is_valid():
            title1 = form.cleaned_data['title1']
            title2 = form.cleaned_data['title2']
            response1 = requests.get(f'{url}?t={title1}&apikey={apikey}')
            response2 = requests.get(f'{url}?t={title2}&apikey={apikey}')
            if response1 and response2:
                movie1 = response1.json()
                movie2 = response2.json()
                if float(movie1['imdbRating'])>float(movie2['imdbRating']):
                    winner = movie1['Title']
                elif float(movie2['imdbRating'])>float(movie1['imdbRating']):
                    winner = movie2['Title']
                else:
                    winner = "It's a tie."
                return render(request, 'movie_comparison.html', {'form': form, 'movie1': movie1, 'movie2': movie2, 'winner': winner})
            else:
                return HttpResponse('<body>No matches found Please make sure entered titles exist.</body>')
    else:
        form = MovieComparison()
    return render(request, 'movie_comparison.html', {'form': form})