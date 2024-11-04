import numpy as np

def apply_white_balance(demosaic_data, temperature=6150):
    if demosaic_data.ndim != 3 or demosaic_data.shape[2] != 3:
        raise ValueError("Input must be a 3D array with three color channels.")

    R = demosaic_data[:, :, 0]
    G = demosaic_data[:, :, 1]
    B = demosaic_data[:, :, 2]

    r_mean = np.mean(R)
    g_mean = np.mean(G)
    b_mean = np.mean(B)

    r_gain = g_mean / r_mean if r_mean != 0 else 1
    b_gain = g_mean / b_mean if b_mean != 0 else 1

    temperature_factor = 1+((temperature-6150) / 7700)
    r_gain *= temperature_factor
    b_gain /= temperature_factor

    R = (R * r_gain).clip(0, 4095)
    B = (B * b_gain).clip(0, 4095)

    white_balanced_image = np.stack([R, G, B], axis=-1).astype(np.uint16)

    return white_balanced_image