from flask import Flask, request, jsonify, render_template

import utils

import logging

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
logger_handler = logging.FileHandler('logs/api.log', encoding='utf-8')
logger_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def main_page():
    items = utils.get_posts_all()
    return render_template("index.html", items=items)


@app.route('/posts/<int:post_pk>')
def post_page(post_pk):

    post = utils.get_post_by_pk(post_pk)
    poster_name = post["poster_name"]
    poster_avatar = post["poster_avatar"]
    pic = post["pic"]
    content = post["content"]
    views_count = post["views_count"]
    pk = post["pk"]

    comments = utils.get_comments_by_post_id(post_pk)
    len_comments = len(comments)

    return render_template("post.html",
                           poster_name=poster_name,
                           pic=pic,
                           poster_avatar=poster_avatar,
                           content=content,
                           pk=pk,
                           views_count=views_count,
                           comments=comments,
                           len_comments=len_comments)


@app.route('/search')
def search_word():
    substr = request.args.get('s', '')
    data = utils.search_for_posts(substr)
    posts = data[:10]
    len_posts = len(posts)
    return render_template("search.html", posts=posts, len_posts=len_posts, substr=substr)


@app.route('/users/<user_name>')
def search_name(user_name):
    try:
        posts = utils.get_posts_by_user(user_name)
        username = user_name
        return render_template("user-feed.html", posts=posts, username=username)
    except ValueError:
        return "Пользователь не найден"


@app.route('/api/posts')
def api_all_posts():
    logger.info("Запрос /api/posts")
    data = utils.get_json()
    return jsonify(data)


@app.route('/api/posts/<int:post_pk>')
def api_post(post_pk):
    logger.info(f"Запрос /api/posts/{post_pk}")
    data = utils.get_post_by_pk(post_pk)
    return jsonify(data)


@app.errorhandler(404)
def page_not_found(error):
    return "Страница не найдена", 404


@app.errorhandler(500)
def page_not_found(error):
    return "Сервер не отвечает", 500


if __name__ == "__main__":
    app.run()
