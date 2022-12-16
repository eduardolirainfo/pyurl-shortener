"""url shortener app using flask
Returns:
    string: generate a short url for a given url from form input on index.html
"""
from flask import Blueprint
from .views import (
    index,
    about,
    your_url,
    redirect_to_url,
    page_not_found,
    session_api,
    url_api,
)

bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule("/", view_func=index)
bp.add_url_rule("/about/", view_func=about)
bp.add_url_rule("/your-url/", methods=["GET", "POST"], view_func=your_url)
bp.add_url_rule("/<string:code>", view_func=redirect_to_url)
bp.add_url_rule("/api/v1/", view_func=session_api)
bp.add_url_rule("/api/v1/url/", view_func=url_api)

bp.register_error_handler(404, page_not_found)
# bp.add_url_rule("/<string:error>/", view_func=page_not_found)


# @bp.errorhandler(404)
# def error_handler(error):
#     return page_not_found(error)


def init_app(app):
    app.register_blueprint(bp)
