from django.shortcuts import render
from django.http import Http404
from .models import Page, NavbarEntry, Toolkit, ToolkitPage, OrgProfile
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

def organizations(request):
    context = {'organizations': Organization.objects.all()}
    return render(request, 'ghu_main/organizations.html', context)
def toolkits(request):
    context = {'toolkits': Toolkit.objects.all(),
               'navbar': NavbarEntry.objects.all()}
    return render(request, 'ghu_main/toolkits.html', context)

def toolkit(request, slug):
    try:
        toolkit = Toolkit.objects.get(slug=slug)
    except Toolkit.DoesNotExist:
        raise Http404()

    context = {'toolkit': toolkit, 'navbar': NavbarEntry.objects.all()}
    return render(request, 'ghu_main/toolkit.html', context)

def toolkitpage(request, toolkit_slug, toolkitpage_slug):
    try:
        toolkitpage = ToolkitPage.objects.get(slug=toolkitpage_slug, toolkit__slug=toolkit_slug)
    except ToolkitPage.DoesNotExist:
        raise Http404()

    context = {'toolkitpage': toolkitpage, 'navbar': NavbarEntry.objects.all()}
    return render(request, 'ghu_main/toolkitpage.html', context)

def org_profile(request, slug):
    try:
        profile = OrgProfile.objects.get(slug=slug)
    except Toolkit.DoesNotExist:
        raise Http404()

    context = {'profiles': profile,
               'navbar': NavbarEntry.objects.all()
               }
    return render(request, 'ghu_main/org_profile.html', context)
