from .models import NavbarEntry

def navbar(request):
    return {'navbar': NavbarEntry.objects.all()}
