from flask import Blueprint, request, jsonify
from services.facial import FacialService
from models.user import Usuario
from extensions import db
from schemas import facial_features_schema

facial_bp = Blueprint('facial', __name__, url_prefix='/api/facial')

@facial_bp.route('/register', methods=['POST'])
def register_facial():
    data = request.get_json()
    user_id = data.get('user_id')
    image_base64 = data.get('image')
    
    if not all([user_id, image_base64]):
        return jsonify({"error": "Se requieren user_id e image"}), 400
    
    # Verificar usuario
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    try:
        # Registrar características faciales
        facial_feature = FacialService.register_facial_features(
            user_id=user_id,
            image_base64=image_base64,
            metadata={
                'registration_type': 'web',
                'angles': ['frontal']
            }
        )
        
        db.session.add(facial_feature)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": facial_features_schema.dump(facial_feature)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@facial_bp.route('/recognize', methods=['POST'])
def recognize_facial():
    image_base64 = request.json.get('image')
    
    if not image_base64:
        return jsonify({"error": "Se requiere imagen"}), 400
    
    try:
        matches = FacialService.recognize_user(image_base64)
        
        if not matches:
            return jsonify({"match": False, "message": "No se encontraron coincidencias"})
        
        best_match = matches[0]
        user = best_match['feature'].usuario
        
        return jsonify({
            "match": True,
            "confidence": 1 - best_match['distance'],
            "user": {
                "id": user.id,
                "name": user.nombre,
                "email": user.correo_electronico
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400