import numpy as np 
from tqdm import tqdm 
import json
import os 
from PIL import Image, ImageDraw
#Download the dataset from IDD or you can clone the github repo https://github.com/Shirish2004/Vegetation-Segmentation.git
dataset = input("Enter the data for which mask has to be created train/val: ")
path1 = input("Enter the path to the leftImg8bit folder: ") # street view images
path2 = input("Enter the path to the gtFine folder: ") # json file of every frame
path3 = input("Enter the path to the output folder where you have to store masks: ")

#Creating Mask of Images

# paths to json and image files
if dataset == 'train':
    json_base_path = path1+'/'+'train'
    image_base_path = path2+'/'+'train'
    output_base_path = path3+'/'+'train'  
elif dataset == 'val':
    json_base_path = path1+'/'+'val'
    image_base_path = path2+'/'+'val'
    output_base_path = path3+'/'+'val' 

# List of common subfolders
common_subfolders = os.listdir(json_base_path)

for subfolder in common_subfolders:
    # Collecting the JSON files
    json_folder_path = os.path.join(json_base_path, subfolder)

    # Path to corresponding image folder
    image_folder_path = os.path.join(image_base_path, subfolder)

    # Making subdirectories for the masks of images in subfolders
    output_folder_path = os.path.join(output_base_path, subfolder)
    os.makedirs(output_folder_path, exist_ok=True)

    # Collecting JSON and image files
    json_files = [f for f in os.listdir(json_folder_path) if f.endswith('_gtFine_polygons.json')]
    image_files = [f for f in os.listdir(image_folder_path) if f.endswith('_leftImg8bit.jpg')]

    # progress bar
    progress_bar = tqdm(total=len(json_files), desc=f'Subfolder: {subfolder}', unit='file', ncols=100)

    # Iterating through JSON files and creating masks
    for json_file in json_files:
        # Extracting the respective image file name from the JSON file name
        image_file_name = json_file.replace('_gtFine_polygons.json', '_leftImg8bit.jpg')
        if image_file_name in image_files:
            # Now follow the same procedure used to create the mask earlier
            with open(os.path.join(json_folder_path, json_file), 'r') as json_file:
                data = json.load(json_file)

            # Load the corresponding image
            image_path = os.path.join(image_folder_path, image_file_name)
            image = Image.open(image_path)
            mask = Image.new('1', image.size, 0)
            draw = ImageDraw.Draw(mask)

            # Iterating through annotations and extracting the vegetation polygons
            for obj in data['objects']:
                if obj['label'] == 'vegetation':#spcify  as per your classes from IDD dataset
                    polygon_points = obj['polygon']
                    if polygon_points:
                        # Convert the list of polygon points to a list of tuples
                        polygon_tuples = [(x, y) for x, y in polygon_points]
                        draw.polygon(polygon_tuples, outline=1, fill=1)

            # Overlap mask on the image to extract the vegetation
            vegetation_image = Image.new('RGB', image.size)
            vegetation_image.paste(image, mask=mask)

            # Save the extracted vegetation image as a mask
            mask_file_name = image_file_name.replace('_leftImg8bit.jpg', '_mask.png')
            mask_path = os.path.join(output_folder_path, mask_file_name)
            vegetation_image.save(mask_path)

            # Updating the progress bar
            progress_bar.update()

    # Close the progress bar for this subfolder
    progress_bar.close()
    print("****************************Process complete****************************")
    print(f"Total {len(json_files)} masks made and stored under the directory {output_folder_path}\n")

# Counting the number of training and validation images
img_training_folder = path1+'/'+'train'
img_validation_folder = path1+'/'+'val'
mask_validation_folder = input("Enter the path to where the training masks are stored: ")
mask_training_folder = input("Enter the path to where the validation masks are stored: ")

img_training_count = 0
img_validation_count = 0
mask_training_count = 0
mask_validation_count = 0

# Function to count images in a folder
def count_images_in_folder(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png']  
    count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                count += 1
    return count


img_training_count = count_images_in_folder(img_training_folder)

img_validation_count = count_images_in_folder(img_validation_folder)

mask_training_count = count_images_in_folder(mask_training_folder)

mask_validation_count = count_images_in_folder(mask_validation_folder)

# Print the counts
print(f"Number of training images: {img_training_count}")
print(f"Number of validation images: {img_validation_count}")
print(f"Number of training masks: {mask_training_count}")
print(f"Number of validation masks: {mask_validation_count}")

# Now the masks and images have been stored but they are under some same sub folders. It slows down the process of our every time to access the data.
# Thus, we can move the images and masks under train and val to common folders as image and annotations

import os
import shutil

# Base paths
image_base_path = path1+'/'+'train'
mask_base_path = mask_training_folder
img_output_base_path = input("Specify the output path where to store images under: ")
annot_output_base_path = input("Specify where to store the masks: ")

# Create output directories
os.makedirs(img_output_base_path, exist_ok=True)
os.makedirs(annot_output_base_path, exist_ok=True)

# List subfolders in the image base path
subfolders = os.listdir(image_base_path)

# Loop through subfolders
for subfolder in subfolders:
    # Getting the list of image files in the current subfolder
    image_subfolder_path = os.path.join(image_base_path, subfolder)
    image_files = [f for f in os.listdir(image_subfolder_path) if f.endswith('_leftImg8bit.jpg')]

    # Looping through image files and find the corresponding mask file
    for image_file in image_files:
        # As mask and image file have initials the same, we check if a corresponding mask exists for an image
        mask_file = image_file.replace('_leftImg8bit.jpg', '_mask.png')
        mask_file_path = os.path.join(mask_base_path, subfolder, mask_file)

        # Check if the mask file exists
        if os.path.exists(mask_file_path):
            # Copying the image to the output folder
            image_source_path = os.path.join(image_subfolder_path, image_file)
            image_destination_path = os.path.join(img_output_base_path, image_file)
            shutil.copy(image_source_path, image_destination_path)

            # Copying the mask to the output folder
            mask_destination_path = os.path.join(annot_output_base_path, mask_file)
            shutil.copy(mask_file_path, mask_destination_path)

print("Training Dataset organization complete.")
 

# Base paths
image_base_path = path1+'/'+'val'
mask_base_path = mask_validation_folder
img_output_base_path = input("Specify the output path where to store validation images under: ")
annot_output_base_path = input("Specify where to store the validation masks: ")

# Create output directories
os.makedirs(img_output_base_path, exist_ok=True)
os.makedirs(annot_output_base_path, exist_ok=True)

# List subfolders in the image base path
subfolders = os.listdir(image_base_path)

# Loop through subfolders
for subfolder in subfolders:
    # Getting the list of image files in the current subfolder
    image_subfolder_path = os.path.join(image_base_path, subfolder)
    image_files = [f for f in os.listdir(image_subfolder_path) if f.endswith('_leftImg8bit.jpg')]

    # Looping through image files and find the corresponding mask file
    for image_file in image_files:
        # As mask and image file have initials the same, we check if a corresponding mask exists for an image
        mask_file = image_file.replace('_leftImg8bit.jpg', '_mask.png')
        mask_file_path = os.path.join(mask_base_path, subfolder, mask_file)

        # Check if the mask file exists
        if os.path.exists(mask_file_path):
            # Copying the image to the output folder
            image_source_path = os.path.join(image_subfolder_path, image_file)
            image_destination_path = os.path.join(img_output_base_path, image_file)
            shutil.copy(image_source_path, image_destination_path)

            # Copying the mask to the output folder
            mask_destination_path = os.path.join(annot_output_base_path, mask_file)
            shutil.copy(mask_file_path, mask_destination_path)

print("Validation Dataset organization complete.")
