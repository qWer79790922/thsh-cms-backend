import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
)

def upload_to_cloudinary(image_file, filename, folder='restaurants'):
    try:
        result = cloudinary.uploader.upload(
            image_file, 
            public_id=filename,
            folder=folder,
            overwrite=True,
            resource_type='image'
        )
        return result['secure_url']
    except Exception as e:
        print("Upload failed:", e)
        return None

def upload_multiple_images(file_list, folder='restaurants'):
    urls = []

    for index, image_file in enumerate(file_list):
        filename = f'image_{index + 1}'  # 或用原始檔名 image_file.name
        try:
            result = cloudinary.uploader.upload(
                image_file,
                public_id=filename,
                folder=folder,
                overwrite=True,
                resource_type='image'
            )
            urls.append(result['secure_url'])
        except Exception as e:
            print(f"Failed to upload image {index + 1}:", e)
            continue

    return urls