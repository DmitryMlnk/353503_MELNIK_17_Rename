# File and archive handling for Lab 3 - Task 2
# Developer: Dmitry Melnik
# Date: May 01, 2025

import zipfile

class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def read_text(self):
        """Read text from a file."""
        with open(self.filename, 'r', encoding='utf-8') as file:
            return file.read()

    def save_results(self, results):
        """Save analysis results to a file."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            for key, value in results.items():
                file.write(f"{key}: {value}\n")

class ArchiveHandler(FileHandler):
    def zip_results(self, source_file, zip_name):
        """Archive the results file."""
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(source_file)

    def get_archive_info(self, zip_name):
        """Get information about the archive."""
        with zipfile.ZipFile(zip_name, 'r') as zipf:
            return zipf.infolist()