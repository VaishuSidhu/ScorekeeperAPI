
import json
import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.drop_all()
        db.create_all()
        test_client = app.test_client()
        yield test_client

def get_token(client):
    resp = client.post('/login', json={'username': 'admin', 'password': 'admin123'})
    assert resp.status_code == 200
    return resp.get_json()['access_token']

def test_flow(client):
    token = get_token(client)

    # Create trader Alice
    r = client.post('/api/scores', json={'traderName': 'Alice', 'score': 100}, headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 201
    # Update with lower score (should not change)
    r = client.post('/api/scores', json={'traderName': 'Alice', 'score': 90}, headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200
    # Update with higher score
    r = client.post('/api/scores', json={'traderName': 'Alice', 'score': 150}, headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200

    # Create Bob
    r = client.post('/api/scores', json={'traderName': 'Bob', 'score': 120}, headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 201

    # Leaderboard default (Top 10)
    r = client.get('/api/leaderboard')
    data = r.get_json()
    assert len(data) == 2
    assert data[0]['traderName'] == 'Alice'  # highest first

    # Rank
    r = client.get('/api/rank/Alice')
    assert r.status_code == 200
    assert r.get_json()['rank'] == 1

    r = client.get('/api/rank/Bob')
    assert r.status_code == 200
    assert r.get_json()['rank'] == 2

    # Stats
    r = client.get('/api/stats')
    stats = r.get_json()
    assert stats['totalTraders'] == 2
    assert stats['highestScore'] == 150
