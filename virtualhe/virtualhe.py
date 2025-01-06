import argparse
import numpy as np
from skimage import io, img_as_float, img_as_ubyte
import matplotlib.pyplot as plt

'''
Virtual H&E implementation based on: https://doi.org/10.1371/journal.pone.0159337
This implementation is not GPU accelerated

The current implementation is only designed to work with 2D images
'''

def apply_histogram_scaling(image, percentile=99.999):
    """
    Apply histogram scaling such that 1 additional pixel per 100,000 is saturated at maximum intensity.
    """
    max_intensity = np.percentile(image, percentile)
    scaled_image = np.clip(image / max_intensity, 0, 1)
    return scaled_image

def generate_virtual_HE(nucleus_path, eosin_path, output_path, display=False):
    """
    Generate a virtual H&E RGB image using the specified nucleus and eosin channels.
    """
    # Load images
    hematoxylin_image = img_as_float(io.imread(nucleus_path))
    eosin_image = img_as_float(io.imread(eosin_path))
    
    # Preprocess images
    hematoxylin_image = apply_histogram_scaling(hematoxylin_image)
    eosin_image = apply_histogram_scaling(eosin_image)

    # Parameters from the document (Table 1)
    beta_values = {
        "hematoxylin": {"red": 0.860, "green": 1.000, "blue": 0.300},
        "eosin": {"red": 0.050, "green": 1.000, "blue": 0.544},
    }

    # Scaling constant
    k = 2.5

    # Compute RGB channels
    R = np.exp(-beta_values["hematoxylin"]["red"] * hematoxylin_image * k) * \
        np.exp(-beta_values["eosin"]["red"] * eosin_image * k)
    G = np.exp(-beta_values["hematoxylin"]["green"] * hematoxylin_image * k) * \
        np.exp(-beta_values["eosin"]["green"] * eosin_image * k)
    B = np.exp(-beta_values["hematoxylin"]["blue"] * hematoxylin_image * k) * \
        np.exp(-beta_values["eosin"]["blue"] * eosin_image * k)

    # Stack RGB channels
    rgb_image = np.stack((R, G, B), axis=-1)

    # Convert to uint8
    rgb_image_uint8 = img_as_ubyte(np.clip(rgb_image, 0, 1))

    # Save the output
    io.imsave(output_path, rgb_image_uint8)

    # Optionally display the image
    if display:
        plt.imshow(rgb_image_uint8)
        plt.axis('off')
        plt.title("Virtual H&E RGB Image (uint8)")
        plt.show()

if __name__ == "__main__":
    # Command-line argument parser
    parser = argparse.ArgumentParser(description="Generate a virtual H&E RGB image from nucleus and eosin channels.")
    parser.add_argument("nucleus", help="Path to the nucleus (hematoxylin) channel image (e.g., nucleus.tif).")
    parser.add_argument("eosin", help="Path to the eosin channel image (e.g., autof.tif).")
    parser.add_argument("output", help="Path to save the output RGB image (e.g., output.tiff).")
    parser.add_argument("--display", action="store_true", help="Display the generated image.")

    args = parser.parse_args()

    # Run the virtual H&E generator
    generate_virtual_HE(args.nucleus, args.eosin, args.output, args.display)
