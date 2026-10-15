from random import randrange

from .models import Opinion


def random_opinion():
    """Вернуть случайное мнение или None, если база пуста."""
    count = Opinion.query.count()
    if count == 0:
        return None
    return Opinion.query.offset(randrange(count)).first()
