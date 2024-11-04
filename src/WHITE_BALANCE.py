import numpy as np

def apply_white_balance(demosiac_data):
    
    if demosiac_data.ndim != 3 or demosiac_data.shape[2] != 3:
        raise ValueError("Input must be a 3D array with three color channels.")

    R = demosiac_data[:, :, 0].astype(np.float32)
    G = demosiac_data[:, :, 1].astype(np.float32)
    B = demosiac_data[:, :, 2].astype(np.float32)
   
    r_mean = np.mean(R)
    g_mean = np.mean(G)
    b_mean = np.mean(B)
    
    r_gain = g_mean / r_mean if r_mean != 0 else 1
    b_gain = g_mean / b_mean if b_mean != 0 else 1

    # Apply gains
    R = (R * r_gain).clip(0, 4095)
    B = (B * b_gain).clip(0, 4095)

    white_balanced_image = np.stack([R, G, B], axis=-1).astype(np.uint16)

    return white_balanced_image