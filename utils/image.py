import base64
import numpy as np
import cv2

def base64_to_image(base64_str):
    """Convierte base64 a imagen numpy"""
    if ',' in base64_str:
        base64_str = base64_str.split(',')[1]
        
    img_bytes = base64.b64decode(base64_str)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("No se pudo decodificar la imagen")
        
    return img