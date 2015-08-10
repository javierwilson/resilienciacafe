from django.db import models
from filer.fields.image import FilerImageField

class Conference(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    text = models.TextField(blank=True,
                                 verbose_name='Autosized textarea',
                                 help_text='Try and enter few some more lines')
    image = FilerImageField(blank=True, null=True, related_name='conference_images')
    image_footer = FilerImageField(blank=True, null=True, related_name='conference_footers')
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name
