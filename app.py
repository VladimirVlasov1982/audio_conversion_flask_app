from io import BytesIO
from flask import Flask, request, send_file
from sqlalchemy.exc import IntegrityError
from config import Config
from models import User, Record
from setup_db import db
from utils import convert_record_to_mp3


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    app.app_context().push()
    return app


app = create_app(Config)


@app.route('/user', methods=['POST'])
def create_user():
    """
    Создаем пользователя и сохраняем его в базе данных.
    """
    name = request.json['name']
    try:
        user = User(name)
        db.session.add(user)
        db.session.commit()
        return {'id': f'{user.id}', 'access_token': f'{user.access_token}'}
    except IntegrityError:
        db.session.rollback()
        return {'error': 'User already exists'}, 400


@app.route('/record', methods=['POST'])
def create_record():
    """
    Получаем id, токен пользователя и файл в формате wav. Конвертируем полученный файл в mp3 и
    сохраняем его в базу данных. Возвращает URL для скачивания записи.
    """
    user_id = request.form['user_id']
    token = request.form['access_token']
    try:
        user = User.query.filter_by(id=user_id, access_token=token).first()
        if user is None:
            return {'error': 'Invalid user id or token'}
    except:
        return {'error': 'User not found'}, 401

    file = request.files['file']
    if file.filename.split('.')[-1].lower() != 'wav':
        return {'error': 'Invalid file format'}, 400

    file_name = file.filename.split('.')[0] + '.mp3'
    mp3_file = convert_record_to_mp3(file.read())
    try:
        new_record = Record(
            filename=file_name,
            user_id=user_id,
            data=mp3_file,
        )
        db.session.add(new_record)
        db.session.commit()
        return {'url': new_record.url}
    except:
        db.session.rollback()
        return {'error': 'Unable to create record'}, 500


@app.route('/record', methods=['GET'])
def get_record():
    """
    Возвращаем файл в формате mp3 по ссылке, которая была сформирована при создании записи в базе данных.
    """
    record_id = request.args.get('id')
    user_id = request.args.get('user')
    record = Record.query.filter_by(id=record_id, user_id=user_id).first()
    if record is None:
        return {'error': 'Record not found'}, 404
    return send_file(BytesIO(record.data), download_name=record.filename, as_attachment=True)


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
