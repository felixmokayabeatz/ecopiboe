import os
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
import time
import sys

class Command(BaseCommand):
    help = (
        "Delete files from uploads folder older than twelve hours.\n"
        "You can edit the command to include your own period. The repo will be public soon and you can get the source code."
    )

    def handle(self, *args, **kwargs):
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        now = datetime.now()
        files_to_delete = []

        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if now - file_mod_time > timedelta(hours=5):
                    files_to_delete.append(file_path)

        total_files = len(files_to_delete)
        if total_files > 0:
            self.stdout.write(self.style.WARNING(f'Total files to be deleted: {total_files}'))

            confirmation = input('Are you sure you want to proceed with deletion of all files? (YES/no): ')
            if confirmation == 'YES':
                for i, file_path in enumerate(files_to_delete):
                    os.remove(file_path)
                    sys.stdout.write(f'\rDeleted file {i + 1}/{total_files}: {file_path}')
                    sys.stdout.flush()
                    time.sleep(0.001) 
                self.stdout.write('\nAll files older than 5 hours have been deleted.')
            else:
                self.stdout.write(self.style.NOTICE('Operation cancelled. No files were deleted. (YES/no ==> CASE SENSITIVE)'))
        else:
            self.stdout.write(self.style.NOTICE('No files older than 5 hours found.'))

    def add_arguments(self, parser):
        pass

    def print_help(self, *args, **kwargs):
        red_bold = '\033[1;31m'
        reset = '\033[0m'
        help_text = f"{red_bold}{self.help}{reset}\n"
        self.stdout.write(help_text + '\n')
