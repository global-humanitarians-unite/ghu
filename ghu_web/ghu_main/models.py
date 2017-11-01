from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from ordered_model.models import OrderedModel
from django.contrib.auth.models import User, Group
from django.conf import settings

# Useful for attempting full-text search on fields
class SearchManager(models.Manager):
    def __init__(self, search_fields):
        super().__init__()
        self.search_fields = search_fields

    def search(self, terms):
        # Currently, field__search='foo' (full text search) is supported
        # only on postgres, but fake it on other backends
        if settings.HAS_FULL_TEXT_SEARCH:
            suffix = '__search'
        else:
            suffix = '__icontains'

        query = None
        for search_field in self.search_fields:
            q = Q(**{search_field + suffix: terms})

            if query is None:
                query = q
            else:
                query = query | q

        return self.filter(query)

class NavbarEntry(OrderedModel):
    URL_CHOICES = (('ghu_main:toolkits', 'Toolkits listing'),
                    ('ghu_main:organizations', 'Organizations'))

    label = models.CharField(max_length=256)
    page = models.ForeignKey('Page', on_delete=models.CASCADE, null=True,
                             blank=True)
    url = models.CharField(max_length=256, verbose_name='Special page',
                           choices=URL_CHOICES, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Navigation bar entry'
        verbose_name_plural = 'Navigation bar entries'

    def __str__(self):
        return '{}, {}, {}'.format(self.label, self.order, self.page)

    def clean(self):
        if (not self.page and not self.url) or (self.page and self.url):
            raise ValidationError('Must specify either a Page or Special '
                                  'page, but not both')

class Page(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=256)
    contents = models.TextField()
    template = models.ForeignKey('PageTemplate', null=True, blank=True)

    def __str__(self):
        return 'Page "{}": /{}/'.format(self.title, self.slug)

class PageTemplate(models.Model):
    name = models.CharField(max_length=256, verbose_name='User-friendly title')
    template = models.CharField(max_length=256, verbose_name='Template to execute')

    def __str__(self):
        return '{} ({})'.format(self.name, self.template)

class Toolkit(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=256)
    summary = models.TextField()

    def __str__(self):
        return 'Toolkit: {}'.format(self.title)

class ToolkitPage(OrderedModel):
    toolkit = models.ForeignKey(Toolkit, related_name='pages')
    slug = models.SlugField()
    title = models.CharField(max_length=256)
    contents = models.TextField()
    order_with_respect_to = 'toolkit'

    class Meta(OrderedModel.Meta):
        unique_together = (('toolkit', 'slug'),)

    def __str__(self):
        return '{}. Order: {}'.format(self.toolkit, self.order)

class OrgProfile(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)
    location = models.CharField(max_length=256, null=True)
    phone = models.CharField(max_length=256)
    summary = models.CharField(max_length=256, null=True)
    description = models.TextField()

    objects = SearchManager(('name', 'summary', 'description'))

    def __str__(self):
        return 'OrgProfile: {}, slug: {}'.format(self.name, self.slug)

class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    phone = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=512, blank=True)
    bio = models.TextField(blank=True)

    def get_group(self):
        if self.user.is_superuser:
            return 'Administrators'
        else:
            # For now, assume user is in only one group
            # XXX Don't
            group = self.user.groups.first()
            return group.name if group else None

    def set_group(self, group):
        if group == 'Administrators':
            # Don't do anything for now; granting admin permissions to
            # anyone is too dangerous
            pass
        else:
            Group.objects.get(name=group).user_set.add(self.user)
