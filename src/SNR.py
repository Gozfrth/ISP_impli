import numpy as np

def calculate_snr(image, roi):
    
    x1, y1, x2, y2 = roi
    roi_region = image[y1:y2, x1:x2]  # Extract the region of interest
    
    mean_signal = np.mean(roi_region)  # Calculate mean signal within the ROI
    std_dev_noise = np.std(roi_region)  # Calculate standard deviation within the ROI
    
    snr = mean_signal / std_dev_noise if std_dev_noise != 0 else 0
    return snr