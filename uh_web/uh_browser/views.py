from django.shortcuts import render
# XXX Remove this when models are finished
from collections import namedtuple

def home(request):
    return render(request, 'uh_browser/home.html', {})

def about(request):
    return render(request, 'uh_browser/about.html', {})

def orgs(request):
    # XXX Remove this when models are finished
    Org = namedtuple('Org', ['name', 'loc', 'categs'])

    ctx = {
        'results': [Org('An Organization', 'Atlanta, GA, United States', ['health', 'seniors', 'education'])]*64,
    }

    return render(request, 'uh_browser/orgs.html', ctx)

def forum(request):
    # XXX Remove this when models are finished
    Categ = namedtuple('Categ', ['name'])

    ctx = {
        # XXX Put these in a fixture instead of hard-coding them
        'categs': [
            Categ('community'),
            Categ('education'),
            Categ('general'),
            Categ('health'),
            Categ('seniors'),
            Categ('women'),
            Categ('youth'),
        ],
    }

    return render(request, 'uh_browser/forum.html', ctx)
