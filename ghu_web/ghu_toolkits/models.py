from django.db import models

class ToolkitSection(models.Model):
    """Stores a toolkit section"""

    name = models.CharField(max_length=32)
    parent = models.ForeignKey('ToolkitSection', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    description = models.CharField(max_length=128)
    icon = models.CharField(max_length=32, blank=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return 'Toolkit Section: {}'.format(self.find_name())

    def find_name(self):
        parents = ''
        if self.parent is not None:
            parents = self.parent.find_name() + ' / '

        return parents + self.name

class Toolkit(models.Model):
    """Stores a toolkit"""

    section = models.ForeignKey('ToolkitSection', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    slug = models.SlugField()
    visible = models.BooleanField(default=True)

    def __str__(self):
        return 'Toolkit {}, section {}'.format(self.title, self.section.name)
