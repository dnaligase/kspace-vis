import base64
import io
import numpy as np

from PIL import Image


# Convert image files to base64 for web
def encode_image(file_path):
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()


# Convert NumPy image to base64 string
def encode_array_to_base64(img_array):
    img = Image.fromarray(np.uint8(img_array), mode='L')
    buff = io.BytesIO()
    img.save(buff, format="PNG")
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")
    return f"data:image/ppg;base64,{encoded}"
