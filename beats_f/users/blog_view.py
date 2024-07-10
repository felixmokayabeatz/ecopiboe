from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import BlogPost

def blog_list(request):
    authors = User.objects.filter(is_staff=True)
    posts = BlogPost.objects.filter(author__in=authors).order_by('-created_at')
    
    for post in posts:
        post.author_full_name = post.author.get_full_name()

    return render(request, 'blog/blog_list.html', {'posts': posts})



def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    post.author_full_name = post.author.get_full_name()
    
    return render(request, 'blog/blog_detail.html', {'post': post})
