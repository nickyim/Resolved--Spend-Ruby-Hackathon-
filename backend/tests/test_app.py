import pytest
from backend.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_post_route(client):
    response = client.post('/test', json={'key': 'value'})
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Data received!'
    assert json_data['data'] == {'key': 'value'}