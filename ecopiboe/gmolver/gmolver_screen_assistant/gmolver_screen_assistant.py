import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
import pyautogui
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import cv2
import numpy as np

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Screen Assistant App')
        self.root.geometry('800x600')
        self.root.configure(bg='#f0f0f0')

        # Initialize variables
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.screenshot_path = None

        # Setup GUI
        self.initUI()
        self.setup_genai()

    def initUI(self):
        # Main display area
        self.text_display = tk.Text(self.root, height=15, width=80, wrap='word', bg='white', fg='black', font=('Arial', 12))
        self.text_display.pack(pady=10)

        # Screenshot preview
        self.screenshot_label = tk.Label(self.root, bg='white', borderwidth=2, relief='groove')
        self.screenshot_label.pack(pady=10, fill=tk.X, padx=20)

        # Input and control buttons
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=10)

        self.input_field = tk.Entry(input_frame, width=60, font=('Arial', 12))
        self.input_field.pack(side=tk.LEFT, padx=5)

        send_button = tk.Button(input_frame, text='Send', command=self.send_message, bg='#4CAF50', fg='white', font=('Arial', 12))
        send_button.pack(side=tk.LEFT, padx=5)

        screenshot_button = tk.Button(input_frame, text='Take Screenshot', command=self.take_screenshot, bg='#2196F3', fg='white', font=('Arial', 12))
        screenshot_button.pack(side=tk.LEFT, padx=5)

        upload_button = tk.Button(input_frame, text='Upload Image/Video', command=self.upload_file, bg='#FF5722', fg='white', font=('Arial', 12))
        upload_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(input_frame, text='Clear Screenshot', command=self.clear_screenshot, bg='#FFC107', fg='black', font=('Arial', 12))
        clear_button.pack(side=tk.LEFT, padx=5)

    def setup_genai(self):
        load_dotenv('.env')
        API_KEY = os.getenv('API_KEY')
        if not API_KEY:
            self.display_message("Error: API key not found. Please set up your .env file correctly.")
            return

        try:
            genai.configure(api_key=API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            self.display_message(f"Error setting up AI model: {str(e)}")

    def send_message(self):
        message = self.input_field.get().strip()
        if message:
            if self.screenshot_path:  # Check if there is a screenshot to process
                try:
                    self.display_message("Uploading and processing screenshot...")
                    self.process_file(self.screenshot_path)
                    self.clear_screenshot()  # Clear the screenshot after processing
                except Exception as e:
                    self.display_message(f"Error processing file: {str(e)}")
            else:
                self.display_message("No screenshot to process.")

            try:
                response = self.model.generate_content(message)
                self.display_message(f"You: {message}")
                self.display_message(f"ChatBot: {response.text}")
            except Exception as e:
                self.display_message(f"Error generating response: {str(e)}")

        self.input_field.delete(0, tk.END)

    def take_screenshot(self):
        # Hide the Tkinter window
        self.root.withdraw()

        # Create a transparent overlay window
        self.overlay = tk.Toplevel(self.root)
        self.overlay.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.overlay.attributes('-topmost', True)
        self.overlay.attributes('-alpha', 0.3)  # Semi-transparent
        self.overlay.configure(bg='gray')

        # Add a Canvas widget to the overlay for drawing
        self.canvas = tk.Canvas(self.overlay, bg='gray', bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events to the Canvas
        self.canvas.bind('<Button-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_mouse_drag(self, event):
        cur_x = event.x_root
        cur_y = event.y_root
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x = event.x_root
        end_y = event.y_root
        self.overlay.destroy()
        self.save_screenshot(self.start_x, self.start_y, end_x, end_y)
        self.display_message("Screenshot taken and saved.")
        self.screenshot_path = 'screenshot.png'
        
        # Show the Tkinter window again
        self.root.deiconify()

    def save_screenshot(self, start_x, start_y, end_x, end_y):
        # Convert screen coordinates to integers
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)

        # Define the region to capture
        region = (min(start_x, end_x), min(start_y, end_y), max(start_x, end_x), max(start_y, end_y))

        # Capture the screenshot using PIL
        screenshot = ImageGrab.grab(bbox=region)
        screenshot.save('screenshot.png')

        # Update the screenshot preview
        self.display_image('screenshot.png')

        # Update the path to the screenshot
        self.screenshot_path = 'screenshot.png'

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Image or Video",
            filetypes=[("Images", "*.png *.jpg *.jpeg"), ("Videos", "*.mp4 *.avi")]
        )
        if file_path:
            file_size = os.path.getsize(file_path)
            if file_size <= 20 * 1024 * 1024:
                file_type = self.get_file_type(file_path)
                if file_type == 'image':
                    self.display_image(file_path)
                elif file_type == 'video':
                    self.display_video(file_path)
                else:
                    self.display_message("Unsupported file type.")
            else:
                self.display_message("File size exceeds 20MB. Please select a smaller file.")

    def get_file_type(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()
        if extension in ['.png', '.jpg', '.jpeg']:
            return 'image'
        elif extension in ['.mp4', '.avi']:
            return 'video'
        else:
            return 'unknown'

    def display_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.thumbnail((800, 600))
            img_tk = ImageTk.PhotoImage(img)
            self.screenshot_label.config(image=img_tk)
            self.screenshot_label.image = img_tk
        except Exception as e:
            self.display_message(f"Error displaying image: {str(e)}")

    def display_video(self, file_path):
        try:
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                self.display_message("Error opening video file.")
                return

            def update_frame():
                ret, frame = cap.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    img.thumbnail((800, 600))
                    img_tk = ImageTk.PhotoImage(img)
                    self.screenshot_label.config(image=img_tk)
                    self.screenshot_label.image = img_tk
                    self.root.after(30, update_frame)
                else:
                    cap.release()
                    self.display_message("Video playback ended.")

            update_frame()
        except Exception as e:
            self.display_message(f"Error displaying video: {str(e)}")

    def clear_screenshot(self):
        self.screenshot_label.config(image='')
        self.screenshot_label.image = None
        self.screenshot_path = None

    def process_file(self, file_path):
        # Placeholder for file processing logic
        self.display_message(f"Processing {file_path}...")

    def display_message(self, message):
        self.text_display.insert(tk.END, f"{message}\n")
        self.text_display.yview(tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
