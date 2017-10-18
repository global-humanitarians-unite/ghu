from django.db import models
from django.core.exceptions import ValidationError
from ordered_model.models import OrderedModel

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

class NavbarEntry(OrderedModel):
    URL_CHOICES = (('ghu_main:toolkits', 'Toolkits listing'),)

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
    email = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return 'OrgProfile: {}, slug: {}'.format(self.name, self.slug)
