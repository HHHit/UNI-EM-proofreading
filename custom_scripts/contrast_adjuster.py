import os
import numpy as np
import h5py
from skimage import exposure
import imageio

# Change the percentile values to change the contrast output
def adjust_contrast(image, lower_percentile=1, upper_percentile=99):
    low, high = np.percentile(image, (lower_percentile, upper_percentile))
    return exposure.rescale_intensity(image, in_range=(low, high))

def main():
    # Original em data file
    input_tiff_file = "/work/public/em_astrocyte_proofreading/8/0/9/em.tif"

    # Output file (MAKE SURE YOU CHANGE THE LOCATION OF EACH NEW PROCESSED EM DATA, OR OLD CONTRAST ADJUSTED FILES WILL BE OVERRIDDEN)
    output_folder = "/home/aaron/Documents/astrocyte_proofreading/contrast_tests"
    
    # Check if the input .tiff file exists
    if not os.path.isfile(input_tiff_file):
        print(f"Error: Input .tiff file '{input_tiff_file}' not found.")
        return

    # Read the series of images using imageio
    astrocyte_mask_list = imageio.mimread(input_tiff_file, memtest=False)

    # Convert the series into a 3D stack
    stack = np.stack(astrocyte_mask_list, axis=0)
    contrasted_boundaries = np.zeros_like(stack)

    # Adjust contrast for each slice
    for idx in range(stack.shape[0]):
        slice_image = stack[idx]

        # Enhance boundaries (make dark)
        boundaries_adjusted = adjust_contrast(slice_image)
        contrasted_boundaries[idx] = boundaries_adjusted

    # Get the filename from the input path (without extension)
    filename = os.path.splitext(os.path.basename(input_tiff_file))[0]

    # Create the output .h5 file path
    output_h5_boundaries_file = os.path.join(output_folder, f"{filename}_boundaries2.h5")

    # Save the contrast-adjusted boundaries as a .h5 file
    with h5py.File(output_h5_boundaries_file, 'w') as hf:
        hf.create_dataset('data', data=contrasted_boundaries, compression='gzip')

if __name__ == "__main__":
    main()
