import os
import time
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Delete bulk CSV files older than X hours"

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=2,
            help='Delete files older than this many hours'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        cutoff_time = time.time() - (hours * 3600)

        folder = os.path.join(settings.MEDIA_ROOT, 'bulk_results')

        if not os.path.exists(folder):
            self.stdout.write(self.style.WARNING("bulk_results folder not found"))
            return

        deleted = 0

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)

            if not os.path.isfile(file_path):
                continue

            if os.path.getmtime(file_path) < cutoff_time:
                try:
                    os.remove(file_path)
                    deleted += 1
                except Exception as e:
                    self.stderr.write(f"Failed to delete {filename}: {e}")

        self.stdout.write(
            self.style.SUCCESS(f"Deleted {deleted} old bulk result files")
        )
