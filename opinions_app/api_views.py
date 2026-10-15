from flask import jsonify, request

from . import app, db
from .models import Opinion
from .views import random_opinion


@app.get('/api/opinions/')
def get_opinions():
    """Вернуть все мнения, при необходимости отфильтрованные по названию."""
    title = request.args.get('title')
    query = Opinion.query
    if title is not None:
        query = query.filter(Opinion.title.ilike(f'%{title}%'))
    return jsonify(opinions=[opinion.to_dict() for opinion in query.all()])


@app.post('/api/opinions/')
def add_opinion():
    """Создать и сохранить новое мнение."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or 'title' not in data or 'text' not in data:
        return jsonify(error='Поля title и text обязательны'), 400

    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify(opinion=opinion.to_dict()), 201


@app.get('/api/opinions/<int:id>/')
def get_opinion(id):
    """Вернуть мнение по идентификатору."""
    opinion = db.session.get(Opinion, id)
    if opinion is None:
        return jsonify(error='Мнение не найдено'), 404
    return jsonify(opinion=opinion.to_dict())


@app.patch('/api/opinions/<int:id>/')
def update_opinion(id):
    """Частично обновить мнение по идентификатору."""
    opinion = db.session.get(Opinion, id)
    if opinion is None:
        return jsonify(error='Мнение не найдено'), 404
    data = request.get_json(silent=True)
    if isinstance(data, dict):
        opinion.from_dict(data)
    db.session.commit()
    return jsonify(opinion=opinion.to_dict())


@app.delete('/api/opinions/<int:id>/')
def delete_opinion(id):
    """Удалить мнение по идентификатору."""
    opinion = db.session.get(Opinion, id)
    if opinion is None:
        return jsonify(error='Мнение не найдено'), 404
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.get('/api/opinions/random/')
def get_random_opinion():
    """Вернуть случайное мнение из базы."""
    opinion = random_opinion()
    if opinion is None:
        return jsonify(error='В базе нет мнений'), 404
    return jsonify(opinion=opinion.to_dict())
