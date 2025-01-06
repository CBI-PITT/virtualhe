# virtualhe

## This tool creates virtual H&E images from fluorescent microscopy data

The implementation is in python, is NOT GPU accelerated, and is based on the following paper:

Giacomelli MG, Husvogt L, Vardeh H,  Faulkner-Jones BE, Hornegger J, Connolly JL, Fujimoto JG. Virtual  Hematoxylin and Eosin Transillumination Microscopy Using  Epi-Fluorescence Imaging. PLoS One. 2016 Aug 8;11(8):e0159337. doi:  10.1371/journal.pone.0159337. PMID: 27500636; PMCID: PMC4976978.



###### Description:

This tool is intended to be called from the command line and take a image of nuclei (vHematoxylin) and a background image (vEosin) like autofluorescence or a fluorescent counterstain like eosin. The output in a 8bit RGB image saved to disk. 

#### Installing:

```bash
# Clone the repo
cd /dir/of/choice
git clone https://github.com/CBI-PITT/virtualhe.git

# Create a virtual environment
# This assumes that you have miniconda or anaconda installed
conda create -n virtualhe python=3.10 -y

# Activate environment and install zarr_stores
conda activate virtualhe
pip install -e /dir/of/choice/virtualhe
```



###### Usage example:

```bash
# First Activate the envionment:
conda activate virtualhe

python /dir/of/choice/virtualhe/virtualhe.py --help

--- BEGIN OUTPUT ---

usage: virtualhe.py [-h] [--display] nucleus eosin output

Generate a virtual H&E RGB image from nucleus and eosin channels.

positional arguments:
  nucleus     Path to the nucleus (hematoxylin) channel image (e.g., nucleus.tif).
  eosin       Path to the eosin channel image (e.g., autof.tif).
  output      Path to save the output RGB image (e.g., output.tiff).

options:
  -h, --help  show this help message and exit
  --display   Display the generated image.

--- END OUTPUT ---

```

- Now we will take 2 images:
  - Nuclear Image (i.e. DAPI, sytox, topro3): /data/images/nucleus_image.tif
  - Background Image (i.e. autofluorescence, eosin): /data/images/background_image.tif
- We want the output image to be located here:
  - /data/images/vhe_output.tif

```bash
# Run this command
python /dir/of/choice/virtualhe/virtualhe.py /data/images/nucleus_image.tif /data/images/background_image.tif /data/images/vhe_output.tif
```

