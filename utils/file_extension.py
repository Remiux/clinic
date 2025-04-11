import os
from pathlib import Path

def get_file_extension(filename):
    file_name = filename.name
    file_extension = Path(file_name).suffix
    return file_extension 