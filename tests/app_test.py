import json

from app import app
import pytest
from utils import get_post_by_pk, get_posts_all
import random


def test_api_post():
    rand_int = random.randint(1, 8)
    path = '/api/posts/' + str(rand_int)

    response = app.test_client().get(path)
    data = json.loads(response.data)

    data_from_file = get_post_by_pk(rand_int)

    real_keys = set(data.keys())
    reference_keys = set(data_from_file.keys())

    assert real_keys == reference_keys
    assert type(data) == dict


def test_api_all_posts():

    response = app.test_client().get('/api/posts')
    data = json.loads(response.data)

    reference_keys = set()
    items = get_posts_all()
    for item in items:
        reference_keys.update(item.keys())

    for dict_ in data:
        real_keys = set(dict_.keys())
        assert real_keys == reference_keys

    assert type(data) == list
