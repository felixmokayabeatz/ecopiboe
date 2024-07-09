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
            self.slug = slugify(self.title)  # Generate slug from title
            queryset = BlogPost.objects.filter(slug=self.slug).exists()
            if queryset:
                counter = 1
                while queryset:
                    new_slug = f'{self.slug}-{counter}'
                    queryset = BlogPost.objects.filter(slug=new_slug).exists()
                    counter += 1
                    if not queryset:
                        self.slug = new_slug
        super().save(*args, **kwargs)