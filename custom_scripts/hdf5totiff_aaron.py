import os
import h5py
import numpy as np
from PIL import Image

# Path to the parent folder containing children folders with HDF5 chunks
parent_folder = '/work/public/em_astrocyte_proofreading/1/1/2/dojo_folder_split_tiff/ids/tiles/w=00000000'

# Output folder for the combined TIFF file
output_folder = '/work/public/em_astrocyte_proofreading/1/1/2/tiff_slices'

# Create a list to store the merged images
merged_images = []

# Iterate over children folders and sort them based on numerical names
child_folders = sorted(os.listdir(parent_folder), key=lambda x: int(x.split('=')[1]))

# Iterate over the sorted children folders
for child_folder in child_folders:
    child_folder_path = os.path.join(parent_folder, child_folder)

    # Create a list to store the merged chunks
    merged_chunks = []

    # Iterate over the four chunks in each child folder
    chunk_positions = [
        'y=00000000,x=00000000',
        'y=00000000,x=00000001',
        'y=00000001,x=00000000',
        'y=00000001,x=00000001'
    ]
    for chunk_pos in chunk_positions:
        chunk_file = os.path.join(child_folder_path, f'{chunk_pos}.hdf5')

        # Load the HDF5 chunk file
        with h5py.File(chunk_file, 'r') as hdf:
            # The only dataset for one singular chunk is 'IdMap'
            dataset_name = 'IdMap'
            data = hdf[dataset_name][()]
            merged_chunks.append(data)

    # Ensure the chunks have the same dimensions
    chunk_shapes = [chunk.shape for chunk in merged_chunks]
    if len(set(chunk_shapes)) != 1:
        raise ValueError("Chunk dimensions are not the same")

    width, height = chunk_shapes[0]

    # Merge the chunks into a single image
    merged_image = np.zeros((height * 2, width * 2), dtype=np.uint8)
    merged_image[:height, :width] = merged_chunks[0]
    merged_image[:height, width:] = merged_chunks[1]
    merged_image[height:, :width] = merged_chunks[2]
    merged_image[height:, width:] = merged_chunks[3]

    # Convert the merged image to PIL Image
    image = Image.fromarray(merged_image)

    # Save the merged image to the list
    merged_images.append(image)

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Combine all merged TIFF files into one TIFF file while maintaining the order by name
output_combined_path = os.path.join(output_folder, 'combined.tif')
merged_images[0].save(output_combined_path, save_all=True, append_images=merged_images[1:])
