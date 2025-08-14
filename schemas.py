from .extensions import ma
from .models.user import Usuario
from .models.facial import FacialFeatures

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        exclude = ('contrasena',)  # No exponer contraseña

class FacialFeaturesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FacialFeatures
        load_instance = True

# Instancias de esquemas
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
facial_features_schema = FacialFeaturesSchema()
facial_features_list_schema = FacialFeaturesSchema(many=True)