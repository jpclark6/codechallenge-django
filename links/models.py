from django.db import models

class Links(models.Model):
  link = models.CharField(max_length=40, null=False)
  slug = models.SlugField(max_length=40, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.link
