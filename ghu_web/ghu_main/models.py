from django.db import models

class Page(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=256)
    contents = models.TextField()

    def __str__(self):
        return 'Page "{}": /{}/'.format(self.title, self.slug)
