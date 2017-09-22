from django.db import models
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
    label = models.CharField(max_length = 256)    
    page = models.ForeignKey('Page', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return '{}, {}, {}'.format(self.label, self.order, self.page)

class Toolkit(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return 'Toolkit Name: {}'.format(self.name)

class ToolkitPage(OrderedModel):
    toolkit = models.ForeignKey(Toolkit)
    page = models.ForeignKey(Page)

    def __str__(self):
        return 'Toolkit: {} ----- Page: {} ------ Order: {}'.format(self.toolkit, self.page, self.order)
