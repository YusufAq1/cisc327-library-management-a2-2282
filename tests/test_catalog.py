import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import os


app = Flask(__name__)
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'test-secret-key'


from routes.catalog_routes import catalog_bp
app.register_blueprint(catalog_bp)

app.template_folder = os.path.join(os.path.dirname(__file__), '../templates')

@pytest.fixture
def client():
    return app.test_client()

def test_index_redirects_to_catalog(client):
    """Test home page redirects to catalog"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/catalog' in response.location
    

