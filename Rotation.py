
import numpy as np


from scipy.misc import imread, imsave
from math import ceil,floor
from PIL import Image
img = imread('slide_20.png')
# angle=0
# imsave('fabio-{}.jpg'.format(angle),rotate_image(img, angle * np.pi / 180 ))

def img_interp(img, scale = 1):

    # angle_rad = pi * angle_deg / 180.0;

    rows, cols, colours = img.shape

    n_rows = int(round(rows * scale, 0))
    n_cols = int(round(cols * scale, 0))

    enlarged_img = np.ones((n_rows, n_cols, colours))

    for i in range(n_rows - 1):
        for j in range(n_cols - 1):
            x_coord = j / scale
            y_coord = i / scale

            xc = int(ceil(x_coord))
            xf = int(floor(x_coord))
            yc = int(ceil(y_coord))
            yf = int(floor(y_coord))

            W_xc = xc - x_coord
            W_xf = x_coord - xf
            W_yc = yc - y_coord
            W_yf = y_coord - yf

            enlarged_img[i, j, :] = 255 - np.around(W_xc * (W_yc * img[yf, xf, :] + W_yf * img[yc, xf, :]) + W_xf * (W_yc * img[yf, xc, :] + W_yf * img[yc, xc, :]), 0)

    return enlarged_img

def rotate_coords(x, y, theta):
   
    s, c = np.sin(theta), np.cos(theta)
    x, y = np.asarray(x) , np.asarray(y) 
    return x * c - y * s , x * s + y * c 

def rotate_image(src, theta, fill=255):
    
    theta = -theta

    sh, sw = src.shape

    cx, cy = rotate_coords([0, sw, sw, 0], [0, 0, sh, sh], theta)

    dw, dh = (int(np.ceil(c.max() - c.min())) for c in (cx, cy))

    dx, dy = np.meshgrid(np.arange(dw), np.arange(dh))

    sx, sy = rotate_coords(dx + cx.min(), dy + cy.min(), -theta)    

    sx, sy = sx.round().astype(int), sy.round().astype(int)

    mask = (0 <= sx) & (sx < sw) & (0 <= sy) & (sy < sh)

    dest = np.empty(shape=(dh, dw), dtype=src.dtype)

    dest[dy[mask], dx[mask]] = src[sy[mask], sx[mask]]

    # dest[dy[~mask], dx[~mask]] = fill

    return dest




img = imread('fabio-45.jpg')
for angle in (45, 75, 90, 120):
    imsave('fabio-45+{}.jpg'.format(angle),rotate_image(img, angle * np.pi / 180 ))
