import os
import numpy as np
from PIL import Image

def overlay_labels(em_folder, label_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all files in the EM data folder
    em_files = sorted(os.listdir(em_folder))
    label_files = sorted(os.listdir(label_folder))

    # Iterate over the files in alphabetical/numerical order
    for em_file, label_file in zip(em_files, label_files):
        # Load the EM data image
        em_image_path = os.path.join(em_folder, em_file)
        em_image = Image.open(em_image_path)

        # Load the label image
        label_image_path = os.path.join(label_folder, label_file)
        label_image = np.asarray(Image.open(label_image_path))
        label_image[np.where(label_image == 1)] = 0
        label_image = Image.fromarray(np.uint8(label_image))
        # Check if the dimensions of the images match
        if em_image.size != label_image.size:
            print(f"Skipping {em_file}: Images do not match in size")
            continue

        # Apply the label image as a mask with black color      
        overlay_image = Image.new('L', em_image.size)

        # Paste the EM data image onto the overlay image
        overlay_image.paste(em_image, (0, 0))

        # Apply the label image as a mask with black color

        overlay_image.paste((0), mask=label_image)

        # Save the result in the output folder
        output_file = os.path.join(output_folder, em_file)
        overlay_image.save(output_file)

        print(f"Processed {em_file}")

    print("Overlaying labels completed!")


em_folder_path = '/work/public/em_astrocyte_proofreading/1/1/1/em_image_sequence'
label_folder_path = '/work/public/em_astrocyte_proofreading/1/1/1/segmentation_label_sequence'
output_folder_path = '/work/public/em_astrocyte_proofreading/1/1/1/overlay_em_data'

overlay_labels(em_folder_path, label_folder_path, output_folder_path)
