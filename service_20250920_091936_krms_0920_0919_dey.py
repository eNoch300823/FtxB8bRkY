# 代码生成时间: 2025-09-20 09:19:36
# folder_structure Organizer.py
"""
A program that organizes a folder's structure by moving files into
subfolders based on file type or other criteria.
"""

import os
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# Constants for file extensions
FILE_TYPES = {
    'documents': ['.doc', '.docx', '.pdf'],
    'images': ['.jpg', '.jpeg', '.png', '.gif'],
    'videos': ['.mp4', '.avi', '.mov'],
    'audio': ['.mp3', '.wav']
}

# Function to organize the folder structure
def organize_folder(folder_path):
    try:
        # Check if the folder exists
        if not os.path.isdir(folder_path):
            raise ValueError(f"The folder {folder_path} does not exist.")

        # Iterate through each file in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Skip directories
            if os.path.isdir(file_path):
                continue

            # Determine the file type
            file_ext = os.path.splitext(file_name)[1].lower()
            for folder_type, extensions in FILE_TYPES.items():
                if file_ext in extensions:
                    # Create a subfolder if it does not exist
                    subfolder_path = os.path.join(folder_path, folder_type)
                    os.makedirs(subfolder_path, exist_ok=True)

                    # Move the file to the subfolder
                    shutil.move(file_path, subfolder_path)
                    break

    except Exception as e:
        return JSONResponse({'error': str(e)})
    return JSONResponse({'message': 'Folder organized successfully.'})

# Create a Starlette application
app = Starlette(
    debug=True,
    routes=[
        Route('/organize/{folder_path:path}', 'organize_folder'),
    ]
)

# Define the endpoint to organize the folder
@app.route('/organize/{folder_path:path}')
async def root(request):
    folder_path = request.path_params['folder_path']
    return await organize_folder(folder_path)
