import os.path
import json
import string
from flask import render_template, request, url_for, redirect, flash


def index():
    """return index.html
    Returns:
        string: return index.html
    """
    return render_template("index.html")


def about():
    """return about.html
    Returns:
        string: return about.html
    """
    return render_template("about.html")


def your_url():
    """return of the post method with url code
       if the method is not post, return to index.html
    Returns:
        string: return
    """
    if request.method == "POST":
        urls = {}
        file_path = os.path.join(os.path.dirname(__file__), "urls.json")
        is_exist = os.path.exists(file_path)

        if is_exist:
            with open(file_path, encoding="utf-8") as urls_file:
                urls = json.load(urls_file)
        if request.form["code"] in urls.keys():
            flash("Short name has already been taken. Select another name")
            return redirect(url_for("webui.index"))

        urls[request.form["code"]] = {"url": request.form["url"]}
        with open(file_path, "w", encoding="utf-8") as url_file:
            json.dump(urls, url_file)
        return render_template("your_url.html", code=request.form["code"])
    else:
        return redirect(url_for("webui.index"))


def redirect_to_url(code):
    """redirect to the url
    Returns:
        string: return redirect to the url
    """
    file_path = exist_path()

    if file_path is not None:
        with open(file_path, encoding="utf-8") as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if "url" in urls[code].keys():
                    return redirect(urls[code]["url"])
    return redirect(url_for("webui.index"))


def exist_path():
    """check if the path exist
    Returns:
        string: return the path
    """
    file_path = os.path.join(os.path.dirname(__file__), "urls.json")
    is_exist = os.path.exists(file_path)
    if is_exist:
        return file_path
    return None
