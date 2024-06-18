import subprocess
import time
import hashlib
import os
from PIL import Image

def run_adb_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
    return stdout.decode('utf-8')

def get_screen_resolution():
    output = run_adb_command("adb shell wm size")
    resolution = output.split()[-1].strip()
    width, height = map(int, resolution.split('x'))
    return width, height

def take_screenshot(screenshot_number):
    device_screenshot_path = f"/data/local/tmp/screenshot_{screenshot_number}.png"
    command = f"adb shell screencap -p {device_screenshot_path}"
    run_adb_command(command)
    print(f"Screenshot {screenshot_number} saved on device as {device_screenshot_path}")
    return device_screenshot_path

def pull_screenshot(device_screenshot_path, local_screenshot_path):
    command = f"adb pull {device_screenshot_path} {local_screenshot_path}"
    run_adb_command(command)
    print(f"Pulled screenshot to {local_screenshot_path}")

def delete_device_screenshot(device_screenshot_path):
    command = f"adb shell rm {device_screenshot_path}"
    run_adb_command(command)
    print(f"Deleted screenshot on device: {device_screenshot_path}")

def crop_screenshot(local_screenshot_path, top_pixels, bottom_pixels):
    image = Image.open(local_screenshot_path)
    width, height = image.size
    cropped_image = image.crop((0, top_pixels, width, height - bottom_pixels))
    cropped_image.save(local_screenshot_path)
    print(f"Cropped screenshot saved as {local_screenshot_path}")

def get_image_hash(screenshot_path):
    with open(screenshot_path, 'rb') as f:
        img_data = f.read()
    return hashlib.md5(img_data).hexdigest()

def scroll_down(height):
    command = f"adb shell input swipe 500 2000 500 100 1500"
    run_adb_command(command)
    print("Scrolled down")

def main():
    os.makedirs('screenshots', exist_ok=True) 
    width, height = get_screen_resolution()
    screenshot_number = 1
    top_pixels_to_remove = 97  
    bottom_pixels_to_remove = 180  

    # initial values

    device_screenshot_path = take_screenshot(screenshot_number)
    local_screenshot_path = f"screenshots/screenshot_{screenshot_number}.png"
    pull_screenshot(device_screenshot_path, local_screenshot_path)
    delete_device_screenshot(device_screenshot_path)
    crop_screenshot(local_screenshot_path, top_pixels_to_remove, bottom_pixels_to_remove)
    hash1 = get_image_hash(local_screenshot_path)

    while True:
        scroll_down(height)
        time.sleep(1)  

        screenshot_number += 1
        device_screenshot_path = take_screenshot(screenshot_number)
        local_screenshot_path = f"screenshots/screenshot_{screenshot_number}.png"
        
        pull_screenshot(device_screenshot_path, local_screenshot_path)
        delete_device_screenshot(device_screenshot_path)
        crop_screenshot(local_screenshot_path, top_pixels_to_remove, bottom_pixels_to_remove)
        hash2 = get_image_hash(local_screenshot_path)

        if hash1 == hash2:
            print("Reached the bottom of the page.")
            break
        else:
            print("Scrolling...")
            hash1 = hash2

        time.sleep(1) 

# DUM - DUM idea

# def delete_bottom_two():
#     directory = "screenshots/"
#     entries = os.listdir(directory)

#     files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]

#     files_to_remove = files[len(files)-2:]
#     for file in files_to_remove:
#         os.remove(directory + file)
    
#     print("deleted last two files epicly")

def remove_last():
    folder_path = 'screenshots'
    screenshots = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith(".png")]
    screenshots.sort(reverse=True)

    old_hash = get_image_hash(screenshots[0])
    to_remove = []
    for i in range(1,len(screenshots)):
        new_hash = get_image_hash(screenshots[i])
        if new_hash == old_hash:
            to_remove.append(screenshots[i-1])
            old_hash = new_hash
        else:
            break

    # print(to_remove)
    for item in to_remove:
        os.remove(item)


if __name__ == "__main__":
    main()
    # delete_bottom_two()
    remove_last()