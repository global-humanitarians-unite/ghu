from django.shortcuts import render

def home(request):
    return render(request, 'uh_browser/home.html', {})

def about(request):
    return render(request, 'uh_browser/about.html', {})

def orgs(request):
    # XXX remove this
    from collections import namedtuple
    Org = namedtuple('Org', ['name', 'loc', 'categs'])

    ctx = {
        'results': [Org('An Organization', 'Atlanta, GA, United States', ['health', 'seniors', 'education'])]*64,
    }

    return render(request, 'uh_browser/orgs.html', ctx)

def forum(request):
    return render(request, 'uh_browser/forum.html', {})
