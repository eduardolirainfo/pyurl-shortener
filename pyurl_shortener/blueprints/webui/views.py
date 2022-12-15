import os.path
import json
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
       if the method is not post, return error message
    Returns:
        string: return
    """
    if request.method == "POST":
        urls = {}
        file_path = os.path.join(os.path.dirname(__file__), "urls.json")
        print(file_path)
        if os.path.exists("urls.json"):
            with open("urls.json") as urls_file:
                urls = json.load(urls_file)
        if request.form["code"] in urls.keys():
            flash("Short name has already been taken. Select another name")
            return redirect(url_for("webui.index"))

        urls[request.form["code"]] = {"url": request.form["url"]}
        with open("urls.json", "w", encoding="utf-8") as url_file:
            json.dump(urls, url_file)
        return render_template("your_url.html", code=request.form["code"])
    else:
        # error = "Something went wrong. This is not valid URL."
        return redirect(url_for("webui.index"))
