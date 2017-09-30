from django.shortcuts import render
from django.http import Http404
from .models import Page, NavbarEntry

def page(request, slug=None):
    if slug is None:
        slug = ''

    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        raise Http404()

    if page.template:
        template = page.template.template
    else:
        template = 'ghu_main/page.html'
    context = {'page': page, 'navbar': NavbarEntry.objects.all()}
    return render(request, template, context)
