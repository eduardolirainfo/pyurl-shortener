import os.path
import json
from flask import (
    render_template,
    request,
    url_for,
    redirect,
    flash,
    abort,
    session,
)


def index():
    """return index.html
    Returns:
        string: return index.html
    """
    return render_template("index.html", codes=session.keys())


def about():
    """return about.html
    Returns:
        string: return about.html
    """
    return render_template("about.html")


def exist_path():
    """check if the path exist
    Returns:
        string: return the path
    """
    file_path = os.path.dirname(__file__)
    file_path = os.path.join(file_path, "instances", "urls.json")
    is_exist = os.path.exists(file_path)

    return (file_path, is_exist)


def your_url():
    """return of the post method with url code
       if the method is not post, return to index.html
    Returns:
        string: return
    """
    if request.method == "POST":
        urls = {}

        file_path, is_exist = exist_path()

        if is_exist:
            with open(file_path, encoding="utf-8") as urls_file:
                urls = json.load(urls_file)

        if request.form["code"] in urls.keys():
            flash("Short name has already been taken. Select another name")
            return redirect(url_for("webui.index"))

        urls[request.form["code"]] = {"url": request.form["url"]}
        with open(file_path, "w", encoding="utf-8") as url_file:
            json.dump(urls, url_file)
            session[request.form["code"]] = True
            url_file.close()
        return render_template("your_url.html", code=request.form["code"])
    else:
        return redirect(url_for("webui.index"))


def redirect_to_url(code):
    """redirect to the url
    Returns:
        string: return redirect to the url
    """
    file_path, is_exist = exist_path()

    if is_exist:
        with open(file_path, encoding="utf-8") as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if "url" in urls[code].keys():
                    return redirect(urls[code]["url"])
    return abort(404)


def page_not_found(error):
    """return page_not_found.html
    Returns:
        string: return page_not_found.html
    """
    code = error.code
    return render_template("page_not_found.html"), code
