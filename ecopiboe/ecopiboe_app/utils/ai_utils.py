import logging
import google.generativeai as genai

def get_book_summary(book_data):
    try:
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        prompt = (
            f"Title: {book_data['title']}\n"
            f"Author: {book_data['author']}\n"
            f"Publish Date: {book_data['publishDate']}\n"
            f"Description: {book_data['description']}\n\n"
            "Please summarize this book in a concise paragraph using your own knowledge from online, keep it under 70 words always."
        )
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        logging.error(f'Error in get_book_summary: {e}')
        return "An error occurred while summarizing the book, or you are trying to access restricted, censored information or explicit content."
    
 
 
 