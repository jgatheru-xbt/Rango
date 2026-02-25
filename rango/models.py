# Here, you store your applications data models -> where you specify the entities and relationships between data 

from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length = 128, unique = True)
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """You override the model's save() method to automatically generate the slug from another field (e.g., the title) before the object is saved to the database."""
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    


class Page(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    title = models.CharField(max_length = 128)
    url = models.URLField()
    views = models.IntegerField(default = 0)

def __str__(self):
        return self.title