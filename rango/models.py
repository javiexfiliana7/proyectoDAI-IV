from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Tapas(models.Model):
    nombre_tapa = models.CharField(max_length=128, unique=True)
    votos = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        #self.slug = slugify(self.name)
        self.slug = slugify(self.nombre_tapa)
        super(Tapas, self).save(*args, **kwargs)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.nombre_tapa

class Bares(models.Model):
    tapa = models.ForeignKey(Tapas)
    nombre_bar = models.CharField(max_length=128)
    direccion = models.CharField(max_length=128)
    n_visitas = models.IntegerField(default=0)


    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.nombre_bar

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
