from django.shortcuts import render

def home(request):
    return render(request, 'ghu-toolkits/home.html', {})
