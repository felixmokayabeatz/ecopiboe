from django.core.management.base import BaseCommand
from django.utils.text import slugify
from ecopiboe_app.blog import BlogPost

class Command(BaseCommand):
    help = 'Populate slugs for existing blog posts'

    def handle(self, *args, **kwargs):
        posts = BlogPost.objects.all()
        for post in posts:
            if not post.slug:
                post.slug = slugify(post.title)
                original_slug = post.slug
                queryset = BlogPost.objects.all()
                slug = original_slug
                counter = 1
                while queryset.filter(slug=slug).exists():
                    slug = f'{original_slug}-{counter}'
                    counter += 1
                post.slug = slug
                post.save()
        self.stdout.write(self.style.SUCCESS('Successfully populated slugs for all blog posts'))
