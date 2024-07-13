# your_app/templatetags/custom_tags.py

from django import template

register = template.Library()

@register.simple_tag
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {file_path}"
