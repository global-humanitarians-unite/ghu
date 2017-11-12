from django.core.exceptions import PermissionDenied
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.http import Http404
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from ghu_global.models import User
from .email import EmailAPI
from .forms import RegisterForm, SearchForm
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
    form = SearchForm(request.GET)
    form.is_valid()
    context = {'organizations': OrgProfile.objects.search(form.cleaned_data['search_terms']),
                'form': form}
    return render(request, 'ghu_main/organizations.html', context)

def toolkits(request):
    context = {'toolkits': Toolkit.objects.all()}
    return render(request, 'ghu_main/toolkits.html', context)

def toolkit(request, slug):
    try:
        toolkit = Toolkit.objects.get(slug=slug)
    except Toolkit.DoesNotExist:
        raise Http404()

    context = {'toolkit': toolkit}
    return render(request, 'ghu_main/toolkit.html', context)

def toolkitpage(request, toolkit_slug, toolkitpage_slug):
    try:
        toolkitpage = ToolkitPage.objects.get(slug=toolkitpage_slug, toolkit__slug=toolkit_slug)
    except ToolkitPage.DoesNotExist:
        raise Http404()

    context = {'toolkitpage': toolkitpage}
    return render(request, 'ghu_main/toolkitpage.html', context)

def org_profile(request, slug):
    try:
        profile = OrgProfile.objects.get(slug=slug)
    except Toolkit.DoesNotExist:
        raise Http404()

    context = {'profiles': profile}
    return render(request, 'ghu_main/org_profile.html', context)

def register(request):
    form = RegisterForm(request.POST if request.method == 'POST' else None)
    ctx = {}

    if request.method == 'POST' and form.is_valid():
        user = form.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = request.build_absolute_uri(reverse('ghu_main:activate', kwargs=dict(token=token, uid=uid)))

        EmailAPI.send_email(subject='Confirm GHU Account',
                            message='Click the following link to confirm your '
                                    'acccount: {}\n\nThanks,\nGHU Staff'
                                    .format(confirm_url),
                            recipients=(user.email,))
    else:
        ctx['form'] = form

    return render(request, 'registration/register.html', ctx)

def activate(request, uid, token):
    """Activate a newly-registered (but inactive) account."""

    uid = urlsafe_base64_decode(uid)
    user = User.objects.get(pk=uid)
    if not user.is_active and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('ghu_main:home')
    else:
        raise PermissionDenied()
