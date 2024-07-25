import google.generativeai as genai
import time
import os
import mimetypes
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FileUploadForm
from .models import UploadedFile
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

if API_KEY is None:
    raise ValueError("No API_KEY Found!")

genai.configure(api_key=API_KEY)

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file_path = uploaded_file.file.path

            # Upload the file to Google Generative AI
            uploaded_genai_file = genai.upload_file(path=file_path)

            # Wait for the file to be processed
            while uploaded_genai_file.state.name == "PROCESSING":
                time.sleep(10)
                uploaded_genai_file = genai.get_file(uploaded_genai_file.name)

            if uploaded_genai_file.state.name == "FAILED":
                return HttpResponse("File processing failed.", status=500)

            # Determine the file type
            file_type, _ = mimetypes.guess_type(file_path)

            # Create the prompt based on the file type
            if file_type and 'image' in file_type:
                prompt = "Describe this image."
            elif file_type and 'video' in file_type:
                prompt = "Describe this video."
            elif file_type and 'text' in file_type:
                with open(file_path, 'r') as file:
                    file_content = file.read()
                prompt = f"Describe this text: {file_content}"
            else:
                prompt = "Describe the content of this file."

            # Set the model to Gemini 1.5 Flash
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

            # Make the LLM request
            response = model.generate_content([prompt, uploaded_genai_file], request_options={"timeout": 600})

            return HttpResponse(response.text)

    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
