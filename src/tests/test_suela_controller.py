import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from src.controllers.suela_controller import suela_bp # Import suela_bp desde suela_controller
from src.app import app  # Ajusta si app está en otro módulo

   # Configuración del cliente de prueba
@pytest.fixture
def client():
       app.config['TESTING'] = True
       app.register_blueprint(suela_bp)  # Asegura que el blueprint esté registrado
       with app.test_client() as client:
           yield client

   # Fixture para mockear la sesión de la base de datos
@pytest.fixture
def mock_db_session():
       with patch('src.models.models.db.session') as mock_session:  # Ajusta si db está en src/models/__init__.py
           # Simula flush para asignar id_suela
           mock_session.flush.side_effect = lambda: setattr(mock_session.add.call_args[0][0], 'id_suela', 1)
           yield mock_session

   # Caso 1: Crear una suela con detalles (Éxito)
def test_create_suela_with_details(client, mock_db_session):
       data = {
           "id_calzado": 1,
           "descripcion_general": "Suela con diseño mixto",
           "detalles": [
               {
                   "id_cuadrante": 1,
                   "id_forma": 1,
                   "detalle_adicional": "Círculos de 1 cm"
               },
               {
                   "id_cuadrante": 2,
                   "id_forma": 2,
                   "detalle_adicional": "Cuadrados en rejilla"
               }
           ]
       }
       response = client.post('/suelas', json=data)
       assert response.status_code == 201
       assert response.json['msg'] == "Suela creada exitosamente"
       assert response.json['suela']['id_suela'] == 1
       assert response.json['suela']['id_calzado'] == 1
       assert response.json['suela']['descripcion_general'] == "Suela con diseño mixto"
       assert len(response.json['suela']['detalles']) == 2
       assert response.json['suela']['detalles'][0]['id_cuadrante'] == 1
       assert response.json['suela']['detalles'][0]['id_forma'] == 1
       assert response.json['suela']['detalles'][0]['detalle_adicional'] == "Círculos de 1 cm"
       assert response.json['suela']['detalles'][1]['id_cuadrante'] == 2
       assert response.json['suela']['detalles'][1]['id_forma'] == 2
       assert response.json['suela']['detalles'][1]['detalle_adicional'] == "Cuadrados en rejilla"
       mock_db_session.add.assert_called()
       mock_db_session.commit.assert_called_once()

 