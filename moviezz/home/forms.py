from django import forms

class InputGenre(forms.Form):
    title = forms.CharField(label='Title Prompt:', max_length=100)
    genre = forms.CharField(label='Genre(Optional):', max_length=30, required=False)

class MovieComparison(forms.Form):
    title1 = forms.CharField(label='Movie 1:', max_length=100)
    title2 = forms.CharField(label='Movie 2:', max_length=100)