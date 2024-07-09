from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
            if not self.slug:
                original_slug = slugify(self.title)
                queryset = BlogPost.objects.all()
                slug = original_slug
                counter = 1
                while queryset.filter(slug=slug).exists():
                    slug = f'{original_slug}-{counter}'
                    counter += 1
                self.slug = slug
            super().save(*args, **kwargs)
