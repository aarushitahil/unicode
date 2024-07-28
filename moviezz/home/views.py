import requests
from django.shortcuts import render

apikey = 'c2ab0e02'
url = 'http://www.omdbapi.com/'

def home(request):
    favorite_movie = 'dil'
    response = requests.get(f'{url}?s={favorite_movie}&apikey={apikey}&page=1')
    movies = response.json().get('Search', [])
    return render(request, 'home/home.html', {'movies': movies})

def movie_details(request, title):
    response = requests.get(f'{url}?t={title}&apikey={apikey}')
    movie = response.json()
    return render(request, 'home/movie_details.html', {'movie': movie})
