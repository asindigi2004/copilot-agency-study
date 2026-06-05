import pytest
from app.routes import app, task_service


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_service():
    # reset the in-memory service between tests
    task_service.tasks = []
    task_service.next_id = 1


def test_get_tasks_empty(client):
    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_task_valid(client):
    resp = client.post('/tasks', json={'title': 'Test task'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['id'] == 1
    assert data['title'] == 'Test task'
    assert data['done'] is False


def test_get_tasks_non_empty(client):
    client.post('/tasks', json={'title': 'A'})
    client.post('/tasks', json={'title': 'B'})
    resp = client.get('/tasks')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['title'] == 'A'


def test_create_task_missing_title(client):
    resp = client.post('/tasks', json={})
    assert resp.status_code == 400
    assert resp.get_json() == {'error': 'title required'}


def test_patch_task_valid_and_invalid(client):
    client.post('/tasks', json={'title': 'To update'})
    resp = client.patch('/tasks/1', json={'done': True})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['id'] == 1
    assert data['done'] is True

    resp_not_found = client.patch('/tasks/999', json={'done': True})
    assert resp_not_found.status_code == 404
    assert resp_not_found.get_json() == {'error': 'not found'}


def test_delete_task_valid_and_invalid(client):
    client.post('/tasks', json={'title': 'To delete'})
    resp = client.delete('/tasks/1')
    assert resp.status_code == 204
    assert resp.data == b''

    resp_not_found = client.delete('/tasks/999')
    assert resp_not_found.status_code == 404
    assert resp_not_found.get_json() == {'error': 'not found'}
