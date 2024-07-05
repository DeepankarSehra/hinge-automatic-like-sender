import shutil
import os

def delete_folder(folder_path):
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"'{folder_path}' deleted epicly.")
    except Exception as e:
        print(f"error: {e}")

folder_paths = ['cropped_text_boxes', 'screenshots', 'profile_elements']

for folder_path in folder_paths:
    delete_folder(folder_path)
