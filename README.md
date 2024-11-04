## BUILDING
```
python -m venv env
```

#### On Ubuntu,
```
source env/bin/activate
```

#### On Windows,
```
env\Scripts\activate.bat
```
```
pip install -r requirements.txt

streamlit run src/HOME.py
```

## REPORT
This report provides an overview of the image processing assignments implemented using Python and Streamlit. The assignments cover various image processing techniques such as `demosaicing, white balance, denoising, gamma correctio and sharpening` in Assignment 1, `median, bilateral filters, AI Denoising, SNR, Laplace Edge enhancement` in Assignment 2 and `HDR Imaging` in Assignment 3.

It is wrapped in a streamlit UI for customizing the tunable parameters that all individual processes have, for example:

![example](https://github.com/Gozfrth/ISP_Impli/blob/main/images/tunable_parameters.png?raw=true "Example")

### Assignment 1: Basic Image Signal Processing (ISP) Impementation
##### Modules and Functions

##### Demosaicing:
![demosaic image](https://github.com/Gozfrth/ISP_Impli/blob/main/images/demosaic.png?raw=true "Demosaic")
- Converts a Bayer CFA to an RGB image using bilinear interpolation. Uses scipy's convolve function to convolve color matrices over CFA and merge the resulting values into rgb format(16b - 12b effective).

###### Tunable Parameters: `r_gain`, `g_gain`, `b_gain`

##### White Balance:
- Adjusts the color balance of an image based on a simple Grey-world Algorithm.Further editing on a user-specified temperature. Scales red and blue gains based on green mean
###### Tunable Parameters: `demosaic_data`, `temperature`

![white balance image](https://github.com/Gozfrth/ISP_Impli/blob/main/images/white_balance.png?raw=true "White balance")

###### Further images in the `/images` directory

##### Denoising:
- Applies a Gaussian filter to reduce noise in the image.
- Uses a custom function to create approximation of Gaussian kernel.
- Uses scipy's convolve function to convolve the kernel over the image.
- Tunable Parameters: `kernel_size`, `sigma`, `scaling_factor`

##### Gamma Correction:
- Applies gamma correction `2.2` and reduces the bit depth of the image `(12b - 8b)`.
###### Tunable Parameters: `gamma`

##### Sharpening:
- Sharpens the image using the unsharp mask technique.
###### Tunable Parameters: `alpha`

### Assignment 2: Advanced Denoising and Filtering

##### Median and Bilateral Filtering:
![median and bilateral](https://github.com/Gozfrth/ISP_Impli/blob/main/images/median_bilateral.png?raw=true "Median and Bilateral Filter (compared with Gaussian)")
- Applies median and bilateral filters to the image. Uses opencv's median and bilateral functions.
###### Tunable Parameters: `kernel_size`

##### AI Denoising:
- Placeholder

##### Signal-to-Noise Ratio (SNR):
- The function computes SNR values for selected regions in a denoised image by calculating the mean signal and noise within each ROI. It displays the marked ROIs on the image and outputs the SNR values for each region.
![SNR](https://github.com/Gozfrth/ISP_Impli/blob/main/images/snr.png?raw=true "SNR")

##### Laplacian Filtering:
- This function uses a Laplacian filter on a grayscale version of the image to detect edges and converts the result to an 8-bit format. The filtered edges are then combined with the original RGB image by adding a weighted blend of the edge information to each color channel. An enhancement factor controls the intensity of the effect, preserving the original colors while highlighting edges.
- Tunable Parameters: `kernel_size`, `enhancement_factor`
![Laplacian Filter](https://github.com/Gozfrth/ISP_Impli/blob/main/images/laplacian_filter_kernel_size_5.png?raw=true "kernel size 5")

##### Edge Strength:
- The function applies a Canny edge detector to a denoised image with user-controlled thresholds, converting it to an 8-bit format before edge detection. It then calculates the edge strength as a percentage of detected edge pixels and displays the edge image.


- Tunable Parameters: `threshold1`, `threshold2` 
![Edge Strength](https://github.com/Gozfrth/ISP_Impli/blob/main/images/edge_strengthened.png?raw=true "Edge Strength")

### Assignment 3: High Dynamic Range (HDR) Imaging
##### HDR Imaging:
- Combines multiple images taken with different exposure times to create an HDR image using Debevec, Robertson, and Mertens methods.
- Outputs the hdr images generated, along with crf :
![crf](https://github.com/Gozfrth/ISP_Impli/blob/main/images/crf.png?raw=true "Crf")
- Inputs: 3 images taken of the same scenario, at different exposure times. The exposure times of each image must be known and input as such:
![hdr input](https://github.com/Gozfrth/ISP_Impli/blob/main/images/hdr_options.png?raw=true "HDR Input") 

##### Utilities
The `UTILS.py` file contains various custom utility functions for image processing, including:

###### Display Functions:
```
display_interactive_plot
display_subplots_2
display_crf
display_color_checker
```

###### Image Conversion:
```
b16_to_b8
```

###### Gaussian Filter:
```
derive_kernel_unnormalized
apply_gaussian_filter_whole
apply_gaussian_filter_per_channel
```

###### Raw Image Loading:
```
load_raw_image
load_raw_image_rgb
```

### Conclusion
This project demonstrates various image processing techniques and provides an interactive user interface for visualizing and adjusting parameters. The use of Streamlit allows for easy exploration and experimentation with different image processing methods.