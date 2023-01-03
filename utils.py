import json

from json import JSONDecodeError


def get_json():
    try:
        with open("data/posts.json", "r", encoding="utf-8") as file:
            posts = json.load(file)
            return posts

    except FileNotFoundError as e:
        return f"{e} Файл не найден"
    except JSONDecodeError as e:
        return f"{e} Файл не удается преобразовать"


def get_posts_all():
    return get_json()


# noinspection PyTypeChecker
def get_posts_by_user(user_name):

    if type(user_name) != str:
        raise TypeError("Агрумент не строка")

    result = []
    for post in get_posts_all():
        result.append(post['poster_name'].lower())

    if user_name.lower() not in result:
        raise ValueError("Пользователь не найден")

    posts_by_name = []
    for post in get_posts_all():
        if post['poster_name'] == user_name:
            posts_by_name.append(post)
    return posts_by_name


def get_comments_from_json():
    try:
        with open("data/comments.json", "r", encoding="utf-8") as file:
            comments_json = json.load(file)
            return comments_json
    except FileNotFoundError:
        return "Файл не найден"
    except JSONDecodeError:
        return "Файл не открыается"


def get_comments_by_post_id(post_id):

    if post_id <= 0:
        raise ValueError("Только целое число")

    if type(post_id) != int or type(post_id) == float:
        raise TypeError("Только целое число")

    existing_ids = []
    for comment in get_comments_from_json():
        existing_ids.append(comment["post_id"])

    if post_id not in existing_ids:
        raise ValueError("Пост не найден")

    comments_by_post_id = []
    for comment in get_comments_from_json():
        if comment["post_id"] == post_id:
            comments_by_post_id.append(comment)

    return comments_by_post_id


def search_for_posts(query):
    if type(query) != str:
        raise TypeError("Только строка")

    posts = []
    for post in get_json():
        if query.lower() in post["content"].lower():
            posts.append(post)
    return posts


def get_post_by_pk(pk):

    if pk <= 0:
        raise ValueError("Только целое число")

    if type(pk) == str or type(pk) == float:
        raise TypeError("Только целое число")

    for post in get_json():
        if post["pk"] == pk:
            return post

