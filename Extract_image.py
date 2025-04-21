import random
import urllib.request
import os
import json
#to get location randomly in a range
def generate_random():
    latitude = random.uniform(21.627508355745825, 21.815849285571183) 
    longitude = random.uniform(39.22923456541662, 39.12710012754746) 
    return latitude, longitude

#check before download image 
def check_image_exists(api_key, latitude, longitude):
    metadata_url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={latitude},{longitude}&key={api_key}"
    response = urllib.request.urlopen(metadata_url)
    data = response.read().decode('utf-8')
    if 'status" : "OK' in data:
        return True
    else:
        return False
    
#using metadat to get the date
def download_gsv_image(api_key, latitude, longitude, heading, pitch, fov, save_directory):
    metadata_url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={latitude},{longitude}&key={api_key}"
    metadata_response = urllib.request.urlopen(metadata_url)
    metadata = json.loads(metadata_response.read().decode('utf-8'))
    date = metadata.get("date")
    
#get the image
    image_url = f"https://maps.googleapis.com/maps/api/streetview?size=640x640&location={latitude},{longitude}&heading={heading}&pitch={pitch}&fov={fov}&key={api_key}"
    image_path = os.path.join(save_folder, f"image_{latitude}_{longitude}_{heading}_{date}.jpg")
    urllib.request.urlretrieve(image_url, image_path)
    print(f"Downloaded image: {image_path}")

# Example 
api_key = ""
num_images = 3000 # Number of images to download
save_folder = "gsv_images"

# Create directory if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
    
# For loop to Download multiple images 
downloaded_images = 0
while downloaded_images < num_images:
    latitude, longitude = generate_random()
    headings = [0, 90, 180, 270]  # North, East, South, West
    pitch = 0
    fov = 90

    if check_image_exists(api_key, latitude, longitude):
        for heading in headings:
            download_gsv_image(api_key, latitude, longitude, heading, pitch, fov, save_folder)
        downloaded_images += 1
        print(f"Downloaded image {downloaded_images}")
    else:
        print(f"Skip")
