from django.db import models

class Link(models.Model):
  link = models.CharField(max_length=100)
  slug = models.SlugField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.link