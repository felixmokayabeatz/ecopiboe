import google.generativeai as genai
import time
import os
import mimetypes
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from .models import UploadedFile
from django.contrib.auth.models import User
from dotenv import load_dotenv
import logging
import uuid

# Load environment variables
load_dotenv()

# Configure API key
API_KEY = os.getenv('API_KEY')
if API_KEY is None:
    raise ValueError("No API_KEY Found!")
genai.configure(api_key=API_KEY)

# Set up logging
logger = logging.getLogger(__name__)

# Allowed MIME types and max upload size
ALLOWED_MIME_TYPES = [
    'text/plain', 'text/html', 'text/css', 'text/javascript', 'application/x-javascript',
    'text/x-typescript', 'application/x-typescript', 'text/csv', 'text/markdown', 'text/x-python',
    'application/x-python-code', 'application/json', 'text/xml', 'application/rtf', 'text/rtf',
    'video/mp4', 'video/mpeg', 'video/mov', 'video/avi', 'video/x-flv', 'video/mpg', 'video/webm',
    'video/wmv', 'video/3gpp', 'audio/wav', 'audio/mp3', 'audio/aiff', 'audio/aac', 'audio/ogg',
    'audio/flac', 'image/png', 'image/jpeg', 'image/webp', 'image/heic', 'image/heif'
]
MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB

# Path to context directory
CONTEXT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'context')

def get_user_context_dir(user):
    user_dir_name = f"{user.id}_{user.first_name}"
    user_context_dir = os.path.join(CONTEXT_DIR, user_dir_name)
    os.makedirs(user_context_dir, exist_ok=True)
    return user_context_dir

def save_context_to_file(user, context):
    user_context_dir = get_user_context_dir(user)
    context_file_name = f"context_{uuid.uuid4().hex}.txt"
    context_file_path = os.path.join(user_context_dir, context_file_name)
    with open(context_file_path, 'w') as context_file:
        context_file.write(context)
    return context_file_path

def get_combined_context(user):
    user_context_dir = get_user_context_dir(user)
    combined_context = ""
    for context_file in os.listdir(user_context_dir):
        context_file_path = os.path.join(user_context_dir, context_file)
        with open(context_file_path, 'r') as file:
            combined_context += file.read() + "\n"
    return combined_context

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        custom_prompt = request.POST.get('custom_prompt', '')

        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Validate file size
            if uploaded_file.size > MAX_UPLOAD_SIZE:
                return render(request, 'upload.html', {
                    'form': form,
                    'error_message': 'File size exceeds 20MB limit.'
                })

            # Validate MIME type
            file_type, _ = mimetypes.guess_type(uploaded_file.name)
            if file_type not in ALLOWED_MIME_TYPES:
                return render(request, 'upload.html', {
                    'form': form,
                    'error_message': 'Unsupported file type.'
                })

            uploaded_file_instance = form.save()
            file_path = uploaded_file_instance.file.path

            try:
                # Upload file to generative AI
                uploaded_genai_file = genai.upload_file(path=file_path)

                while uploaded_genai_file.state.name == "PROCESSING":
                    time.sleep(10)
                    uploaded_genai_file = genai.get_file(uploaded_genai_file.name)

                if uploaded_genai_file.state.name == "FAILED":
                    return HttpResponse("File processing failed.", status=500)

                # Determine prompt based on file type
                if 'image' in file_type:
                    file_prompt = "Describe this image in an educational context."
                elif 'video' in file_type:
                    file_prompt = "Describe this video in an educational context."
                elif 'text' in file_type:
                    with open(file_path, 'r') as file:
                        file_content = file.read()
                    file_prompt = f"Summarize and explain this text for study purposes: {file_content}"
                else:
                    file_prompt = "Describe the content of this file in an educational context."

                prompt = f"{custom_prompt}\n\n{file_prompt}" if custom_prompt else file_prompt

                # Combine with previous context
                combined_context = get_combined_context(request.user)
                full_prompt = combined_context + "\n" + prompt

                model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

                response = model.generate_content([full_prompt, uploaded_genai_file], request_options={"timeout": 600})

                # Save response to context file
                save_context_to_file(request.user, response.text)

                return render(request, 'upload.html', {
                    'form': form,
                    'response_text': response.text
                })

            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")
                return render(request, 'upload.html', {
                    'form': form,
                    'error_message': f"An error occurred while processing your request. Please try again later."
                })

    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
