from django import forms

class SearchForm(forms.Form):
    search_terms = forms.CharField(label = 'Search', max_length = 100, required = False)
