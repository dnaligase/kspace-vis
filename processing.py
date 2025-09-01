import numpy as np

from tqdm import tqdm
from PIL import Image
from itertools import product
from scipy.fft import fft2, fftshift
from typing import cast


def process_image(path: str):
    image = Image.open(path)
    # Resize the image
    image = image.resize((86, 86))

    # img to array
    img = np.array(cast(Image, image))[:, :, 0]
    print(f"Setting image shape to ({img.shape})\nmin-max: {img.min(), img.max()}")
    rows, cols = img.shape

    kl = list(product(np.arange(len(img)), repeat=2))
    coefs = np.zeros(len(kl), dtype=np.complex64)
    bars = np.zeros((rows, cols, len(kl)), dtype=np.complex64)

    i = np.arange(rows).reshape(-1, 1)
    j = np.arange(cols).reshape(1, -1)

    for _, (k, l) in enumerate(tqdm(kl, desc='Applying manual DFT...')):
        exponent = -2j * np.pi * ((k * i / rows) + (l * j / cols))
        bars[:, :, _] = np.exp(exponent)
        coefs[_] = np.sum(img * np.exp(exponent))

    images = np.real(bars * coefs)
    y = fft2(img)
    fourier_im = fftshift(y)

    X_std = (images - images.min(axis=(0, 1))) / (images.max(axis=(0, 1)) - images.min(axis=(0, 1)) + 1e-5)
    X_scaled = X_std * (255 - 0) + 0

    X_scaled[:, :, 0] = img.mean()

    # data
    grid_data = np.log2(np.abs(fourier_im))
    idx_mat = np.arange(grid_data.shape[0] * grid_data.shape[1]).reshape(grid_data.shape)
    idx_mat_shifted = fftshift(idx_mat)

    imgs = X_scaled[:, :, idx_mat_shifted.flatten()]

    return images, imgs, idx_mat, idx_mat_shifted, grid_data
