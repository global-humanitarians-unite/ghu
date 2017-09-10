from django.db import models

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
