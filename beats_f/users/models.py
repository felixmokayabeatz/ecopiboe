from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class UploadFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('text', 'Text'),
        ('code', 'Code'),
    ]

    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    
    
class Userinfo(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class ChatBot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Other fields
    
    text_input = models.CharField(max_length=500)
    gemini_output = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.text_input

class EcoFootprintCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EcoFootprintQuestion(models.Model):
    category = models.ForeignKey(EcoFootprintCategory, on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text
    
class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(EcoFootprintQuestion, on_delete=models.CASCADE)
    response = models.TextField()
    date = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.user.username}'s response to {self.question}"
    
class AIResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s AI Result"
    
    
