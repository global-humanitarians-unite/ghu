from django.shortcuts import render

def home(request):
    return render(request, 'uh_browser/home.html', {})

def about(request):
    return render(request, 'uh_browser/about.html', {})

def orgs(request):
    return render(request, 'uh_browser/orgs.html', {})

def forum(request):
    return render(request, 'uh_browser/forum.html', {})
