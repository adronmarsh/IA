import zipfile
import os

# Path to the uploaded file
zip_file_path = 'D:\Clase\IA\Projects\ChatBot2.zip'
extract_folder_path = 'D:\Clase\IA\Projects\Exrtacted'

# Unzipping the file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder_path)

# Listing the contents of the extracted folder
extracted_files = os.listdir(extract_folder_path)
extracted_files
