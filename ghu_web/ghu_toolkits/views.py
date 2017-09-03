from django.shortcuts import render

def home(request):
    return render(request, 'ghu_toolkits/home.html', {})
