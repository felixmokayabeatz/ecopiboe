

from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import UploadFile
import os

@shared_task
def delete_file_task(file_id):
    try:
        file = UploadFile.objects.get(pk=file_id)
        file_path = file.file.path

        # Ensure the file exists and delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            file.delete()

        print(f"Deleted file {file_id} successfully.")
    except UploadFile.DoesNotExist:
        print(f"File {file_id} does not exist.")
    except Exception as e:
        print(f"Failed to delete file {file_id}: {str(e)}")


@shared_task
def delete_file_after_delay(file_path):
    import time
    time.sleep(4 * 60 * 60)  # 4 hours delay
    
    # Delete the file from the file system
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Optionally, delete the file object from the database
    # Example: Assuming UploadFile model has a 'file_path' field
    try:
        file_obj = UploadFile.objects.get(file_path=file_path)
        file_obj.delete()
    except UploadFile.DoesNotExist:
        pass  # Handle if file object does not exist
