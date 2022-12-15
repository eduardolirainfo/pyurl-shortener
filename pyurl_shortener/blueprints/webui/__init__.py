"""url shortener app using flask
Returns:
    string: generate a short url for a given url from form input on index.html
"""
from flask import Blueprint
from .views import index, about, your_url

bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule("/", view_func=index)
bp.add_url_rule("/about/", view_func=about)
bp.add_url_rule("/your-url/", methods=["GET", "POST"], view_func=your_url)


def init_app(app):
    app.register_blueprint(bp)
