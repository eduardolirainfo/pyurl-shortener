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
)  # noqa E501


def index():
    """return index.html
    Returns:
        string: return index.html with the codes in the session
    """
    is_exist = exist_path()[1]
    list_code = []

    if not is_exist:
        session.clear()
    else:
        with open(exist_path()[0], encoding="utf-8") as urls_file:
            urls = json.load(urls_file)
            urls_file.close()
            # print session id and keys in the session

            for code in urls.keys():
                if code not in session.keys():
                    session[code] = False
                else:
                    if session[code]:
                        list_code.append(code)

    return render_template("index.html", codes=list_code)  # noqa E501


def about():
    """return about.html
    Returns:
        string: return about.html
    """
    return render_template("about.html")


def exist_path():
    """check if the path exist
    Returns:
        string: return the path and if the path exist
    """
    file_path = os.path.dirname(__file__)
    file_path = os.path.join(file_path, "instances", "urls.json")
    is_exist = os.path.exists(file_path)

    return (file_path, is_exist)


def your_url():
    """return of the post method with url code
       if the method is not post, return to index.html
    Returns:
        string: return your_url.html with the code
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
        # else:
        #     session[request.form["code"]] = False
        #     session.clear()

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
        string: return redirect to the url or abort 404
    """
    file_path, is_exist = exist_path()

    if is_exist:
        with open(file_path, encoding="utf-8") as urls_file:
            urls = json.load(urls_file)
            urls_file.close()
            if code in urls.keys():
                if "url" in urls[code].keys():
                    if "http" not in urls[code]["url"]:
                        return redirect("http://" + urls[code]["url"])

                    if code in session.keys():
                        session[code] = True
                    else:
                        session[code] = False

                    return redirect(urls[code]["url"])
    return abort(404)


def page_not_found(error):
    """return page_not_found.html
    Returns:
        string: return page_not_found.html with the code
    """
    code = error.code
    return render_template("page_not_found.html"), code


def session_api():
    """return the session keys
    Returns:
        string: return the session keys in json format
    """
    return {"code": list(session.keys())}


def url_api():
    """return the urls keys
    Returns:
        string: return the urls keys in json format
    """
    file_path, is_exist = exist_path()
    urls = {}
    if is_exist:
        with open(file_path, encoding="utf-8") as urls_file:
            urls = json.load(urls_file)
            urls_file.close()
            list_url = []
            for code in urls.keys():
                if code in session.keys() and session[code]:
                    list_url.append(
                        " { 'code' : "
                        + f"'{code}'"
                        + " , 'url' : "
                        + f" '{urls[code]['url']}'"
                        + " }"
                    )
            return {"url_shortener": list_url}
    return {"code": []}
