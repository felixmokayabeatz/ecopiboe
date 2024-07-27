import os
import json
from PIL import Image
import wave
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

if API_KEY is None:
    print("No API_KEY Found!")
    exit(1)  # Exit if API_KEY is not found

genai.configure(api_key=API_KEY)

# Correct model initialization
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def text():
    chat = model.start_chat(history=[])
    
    # Send initial prompt
    response = chat.send_message("Hello, who are you, and what is 1 + 1?")
    print(response.text)
    
    # Continue the conversation
    response = chat.send_message("Can you tell me more?")
    print(response.text)

    # Example of how to use generate_content with the chat interface
    # You don't need to use model.generate_content inside send_message
    response = chat.send_message("Can you generate some content for me?")
    generated_response = model.generate_content(response.text)
    print(generated_response.text)

def image():
    image_path = 'C:\\Programming\\gemniLearn\\images\\felix.JPG'
    if not os.path.isfile(image_path):
        print(f"Image file not found at {image_path}")
        return
    
    img = Image.open(image_path)
    prompt = "Can you guess what is in the image?"

    response = model.generate_content([prompt, img])
    print(response.text)

def audio():
    audio_path = 'C:\\Programming\\gemniLearn\\audio\\audio.wav'
    if not os.path.isfile(audio_path):
        print(f"Audio file not found at {audio_path}")
        return
    
    try:
        with wave.open(audio_path, 'rb') as wav_file:
            frames = wav_file.readframes(-1)
            params = wav_file.getparams()
            mime_type = f"audio/wav; rate={params.framerate}"
            audio_data = frames

        prompt = "Describe the sound you hear."
        response = model.generate_content([prompt, {'mime_type': mime_type, 'data': audio_data}])
        print(response.text)
    
    except Exception as e:
        print(f"Error reading or processing audio file: {e}")

def generate_json_response():
    import typing_extensions as typing

    class Recipe(typing.TypedDict):
        recipe_name: str

    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

    result = model.generate_content(
        "List 5 popular cookie recipes",
        generation_config=genai.GenerationConfig(response_mime_type="application/json",
                                                 response_schema=list[Recipe])
    )
    print(result.text)

def upload():
    mp3_path = 'audio.mp3'  # Path to your MP3 file
    display_name = 'Sample Audio'

    # Upload the MP3 file
    sample_file = genai.upload_file(path=mp3_path, display_name=display_name)
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    # Save file details to JSON for future reference
    file_details = {
        "name": sample_file.name,
        "uri": sample_file.uri,
        "display_name": sample_file.display_name
    }
    with open('sample_file_details.json', 'w') as f:
        json.dump(file_details, f)

# Function to load uploaded file details
def load_file_details():
    try:
        with open('sample_file_details.json', 'r') as f:
            file_details = json.load(f)
            return {
                "name": file_details['name'],
                "uri": file_details['uri'],
                "display_name": file_details['display_name']
            }
    except FileNotFoundError:
        print("File details not found. Please upload the file first.")
        return None

def seefile():
    # Load the uploaded file details
    sample_file = load_file_details()
    if sample_file is None:
        return
    
    try:
        # Here you can print the details of the loaded file
        print(f"Retrieved file '{sample_file['display_name']}' as: {sample_file['uri']}")
    except Exception as e:
        print(f"Error retrieving file: {e}")

def generate_content():
    # Initialize the Gemini model
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    # Load the uploaded file details
    sample_file = load_file_details()
    if sample_file is None:
        return

    # Generate content using the uploaded file's URI
    prompt = [sample_file['uri'], "Describe the audio with a creative description."]
    response = model.generate_content(prompt)

    # Print the response
    print("Generated content:")
    print(response.text)

def main():
    print("Select any one: \n 1. Text \n 2. Image \n 3. Json \n 4. Audio \n 5. Upload \n 6. See File")
    a = int(input())

    if a == 1:
        text()
    elif a == 2:
        image()
    elif a == 3:
        generate_json_response()
    elif a == 4:
        audio()
    elif a == 5:
        upload()
    elif a == 6:
        seefile()
    elif a == 7:
        generate_content()
    else:
    
        print("Invalid selection")

if __name__ == "__main__":
    main()


