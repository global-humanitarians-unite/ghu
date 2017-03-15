from django.shortcuts import render
# XXX Remove these when models are finished
from collections import namedtuple
Org = namedtuple('Org', ['name', 'loc', 'categs'])
Categ = namedtuple('Categ', ['name'])
# XXX Put these in a fixture instead of hard-coding them
categs = [
    Categ('community'),
    Categ('education'),
    Categ('general'),
    Categ('health'),
    Categ('seniors'),
    Categ('women'),
    Categ('youth'),
]

def home(request):
    return render(request, 'uh_browser/home.html', {})

def about(request):
    return render(request, 'uh_browser/about.html', {})

def orgs(request):
    # XXX Remove this when models are finished

    ctx = {
        'results': [Org('An Organization', 'Atlanta, GA, United States', categs)]*64,
    }

    return render(request, 'uh_browser/orgs.html', ctx)

def forum(request):
    # XXX Remove this when models are finished

    ctx = {
        'categs': categs,
    }

    return render(request, 'uh_browser/forum.html', ctx)
