from PIL import Image
import os

def combine_screenshots(folder, output_image, crop_height):
    screenshots = [img for img in os.listdir(folder) if img.endswith(".png")]
    screenshots.sort()  
    if screenshots[0] == "masti.png":
        os.remove('screenshots/masti.png')
    # screenshots = screenshots[1:4]

    images = []
    for i, img in enumerate(screenshots):
        image = Image.open(os.path.join(folder, img))
        if i != 0:  
            image = image.crop((0, crop_height, image.width, image.height))
        images.append(image)

    width = images[0].width
    total_height = sum(image.height for image in images)

    combined_image = Image.new("RGB", (width, total_height))

    y_offset = 0
    for image in images:
        combined_image.paste(image, (0, y_offset))
        y_offset += image.height

    combined_image.save(output_image)
    print(f"Combined image saved as {output_image}")

combine_screenshots("screenshots", "screenshots/masti.png", crop_height=123)
