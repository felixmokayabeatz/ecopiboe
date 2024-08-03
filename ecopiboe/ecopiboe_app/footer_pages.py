from django.shortcuts import render
from django.conf import settings
import os

def about_us(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'about_content_text/about_content_text.txt')
    with open(file_path, 'r') as file:
        content = file.read()
    return render(request, 'footer/about_us.html', {'content': content})

def careers(request):
    return render(request, 'footer/careers.html')

def contact_us(request):
    return render(request, 'footer/contact_us.html')

def blog(request):
    return render(request, 'footer/blog.html')

def whitepapers(request):
    return render(request, 'footer/whitepapers.html')

def case_studies(request):
    return render(request, 'footer/case_studies.html')

def help_center(request):
    return render(request, 'footer/help_center.html')

def faqs(request):
    return render(request, 'footer/faqs.html')

def support_services(request):
    return render(request, 'footer/support_services.html')


def terms(request):
    file_path = os.path.join('static', 'texts/terms.txt')
    with open(file_path, 'r') as file:
        text = file.read()
    text = text.replace('[Google\'s Rules and Terms]', '<a href="https://policies.google.com/" target="_blank">Google\'s Rules and Terms</a>')

    return render(request, 'terms/terms.html', {'rules_text': text})

