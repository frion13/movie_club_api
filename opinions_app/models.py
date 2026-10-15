from datetime import datetime, timezone

from opinions_app import db


class Opinion(db.Model):
    """Мнение пользователя о фильме."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, nullable=False, unique=True)
    source = db.Column(db.String(256), nullable=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc),
    )
    added_by = db.Column(db.String(64), nullable=True)

    def to_dict(self):
        """Преобразовать мнение в словарь для JSON-ответа."""
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'source': self.source,
            'timestamp': self.timestamp,
            'added_by': self.added_by,
        }

    def from_dict(self, data):
        """Обновить разрешённые поля значениями из словаря."""
        for field in ('title', 'text', 'source', 'added_by'):
            if field in data:
                setattr(self, field, data[field])
