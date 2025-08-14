import numpy as np
import cv2
import insightface
from models.facial import FacialFeatures
from utils.image import base64_to_image

# Inicializamos el modelo de InsightFace solo una vez
_face_model = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])
_face_model.prepare(ctx_id=-1)  # -1 = CPU, si tienes GPU pon 0

class FacialService:
    @staticmethod
    def register_facial_features(user_id, image_base64, metadata=None):
        # Convertir imagen desde base64
        image = base64_to_image(image_base64)
        
        # InsightFace espera imágenes en BGR (como OpenCV)
        faces = _face_model.get(image)
        
        if not faces:
            raise ValueError("No se detectó ningún rostro")
        
        # Tomamos el primer rostro encontrado
        embedding = faces[0].embedding  # Es un vector NumPy de 512 dimensiones
        
        # Guardar en base de datos
        facial_feature = FacialFeatures(
            usuario_id=user_id,
            facial_vector=embedding.tolist(),
            metadata=metadata or {}
        )
        
        return facial_feature

    @staticmethod
    def recognize_user(image_base64, threshold=0.6):
        # Convertir imagen
        image = base64_to_image(image_base64)
        
        # Detectar rostro y obtener embedding
        faces = _face_model.get(image)
        if not faces:
            raise ValueError("No se detectó ningún rostro")
        
        face_encoding = faces[0].embedding
        
        # Buscar coincidencias en la base de datos
        all_features = FacialFeatures.query.all()
        matches = []
        
        for feature in all_features:
            stored_vector = np.array(feature.facial_vector)
            distance = np.linalg.norm(face_encoding - stored_vector)  # Distancia Euclidiana
            
            if distance < threshold:
                matches.append({
                    'feature': feature,
                    'distance': distance
                })
        
        # Ordenar por mejor coincidencia
        matches.sort(key=lambda x: x['distance'])
        
        return matches
