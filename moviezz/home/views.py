import requests
from django.shortcuts import render, redirect
from django import forms

apikey = 'c2ab0e02'
url = 'http://www.omdbapi.com/'

class InputGenre(forms.Form):
    title = forms.CharField(label='Title Prompt:', max_length=30)
    genre = forms.CharField(label='Genre(Optional):', max_length=30, required=False)

def home(request):
    if request.method == 'POST':
        form = InputGenre(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            genre = form.cleaned_data['genre']
            if genre:
                return redirect('searchbygenre', title=title, genre=genre)
            else:
                return redirect('searchbytitle', title=title)
    else:
        form = InputGenre()
    return render(request, 'home.html', {'form': form})

def search_by_title(request, title):
    response = requests.get(f'{url}?s={title}&apikey={apikey}&page=1')
    movies = response.json().get('Search', [])
    return render(request, 'searchbytitle.html', {'movies': movies, 'title': title})

def search_by_genre(request, title, genre):
    response = requests.get(f'{url}?s={title}&apikey={apikey}&page=1')
    all = response.json().get('Search', [])
    genre_movies = []
    for movie in all:
        movie_details = requests.get(f'{url}?i={movie["imdbID"]}&apikey={apikey}').json()
        if genre.lower() in movie_details['Genre'].lower():
            genre_movies.append(movie)
    return render(request, 'searchbygenre.html', {'movies': genre_movies, 'genre': genre, 'title': title})

def movie_details(request, title):
    response = requests.get(f'{url}?t={title}&apikey={apikey}')
    movie = response.json()
    return render(request, 'movie_details.html', {'movie': movie})

