import pytest
from app import app
from models import User, Record
from setup_db import db
import os


@pytest.fixture
def test_user():
    user = User(name="test user")
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()


@pytest.fixture
def wav_file():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'test.wav'))


@pytest.fixture
def client():
    return app.test_client()


def test_create_user(client):
    # Проверяем создание пользователя в базе данных
    response = client.post('/user', json={'name': 'Test'})
    assert response.status_code == 200

    user = User.query.filter_by(name='Test').first()
    assert user is not None

    expected_response = {
        'access_token': user.access_token,
        'id': str(user.id),
    }
    assert response.json == expected_response

    db.session.delete(user)
    db.session.commit()


def test_create_and_get_record(client, wav_file, test_user):
    # Проверяем создание записи в базе данных
    with open(wav_file, "rb") as wav_pf:
        response = client.post('/record',
                               data={
                                   'user_id': test_user.id,
                                   'access_token': test_user.access_token,
                                   'file': (wav_pf, 'test.wav')},
                               )
        assert response.status_code == 200
        assert 'url' in response.json
        record = Record.query.filter_by(user_id=test_user.id).first()
        url = response.json['url']

    # Проверяем возрат файла по ссылке, полученной в запросе post
    response = client.get(url)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'audio/mpeg'
    db.session.delete(record)
    db.session.commit()
