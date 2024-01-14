import subprocess
import json
import base64

from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template(
        "base.html",
        title="Robots.txt parser based on Google's open source parser from Will Critchlow, CEO of SearchPilot",
        form="form",
        desc="My interpretation of how Google parses robots.txt files using a fork of their robust open source parser",
        canonical="/",
    )


def cpp_parse(robots, ua, url):
    if (
        ua.lower() == "googlebot-image"
        or ua.lower() == "googlebot-news"
        or ua.lower() == "googlebot-video"
    ):
        ua = ua + ",googlebot"
    result = subprocess.run(
        [
            #"./robots-OSX-x86_64",
            "./robots-linux",
            base64.b64encode(robots.encode("utf-8")),
            base64.b64encode(ua.encode("utf-8")),
            base64.b64encode(url.encode("utf-8")),
        ],
        stdout=subprocess.PIPE,
    )
    allowed_json = result.stdout.decode("utf-8")
    allowed_list = json.loads(allowed_json)
    allowed = allowed_list["allowed"]
    line = allowed_list["line"]
    allowed_ignore_global = allowed_list["allowed_ignore_global"]
    if (
        ua.lower() == "adsbot-google"
        or ua.lower() == "adsbot-google-mobile"
        or ua.lower() == "mediapartners-google"
    ):
        ignore_global = True
        if allowed != allowed_ignore_global:
            line = 0
            allowed = allowed_ignore_global
    else:
        ignore_global = False
    return {"line": line, "allowed": allowed, "ignore_global": ignore_global}


@app.route("/parse/", methods=["POST"])
def parse():
    robots = request.form["robots"]
    ua = request.form["ua"]
    if ua.lower() == "other":
        ua = request.form["other"]
    url = request.form["url"]
    result = cpp_parse(robots, ua, url)
    line = result["line"]
    allowed = result["allowed"]
    ignore_global = result["ignore_global"]
    robots_highlight = []
    for robots_line in robots.splitlines():
        robots_highlight.append(robots_line)
    return render_template(
        "base.html",
        title="Results of parsing | Will Critchlow's robots.txt parser",
        ua=ua,
        robots=robots_highlight,
        line=line,
        allowed=allowed,
        url=url,
        ignore_global=ignore_global,
        desc="Parsing results from Will Critchlow's interpretation of how Google parses robots.txt files",
        canonical="/parse/",
    )


@app.route("/api/parse/", methods=["POST"])
def parse_api():
    input = request.get_json()
    if not ("robots" in input and "ua" in input and "url" in input):
        return (
            jsonify(
                {"Error": "Missing input - need to supply 'robots', 'ua', and 'url'"}
            ),
            400,
        )
    result = cpp_parse(input["robots"], input["ua"], input["url"])
    return jsonify(result)


@app.errorhandler(404)
def page_not_found(error):
    return (
        render_template(
            "base.html",
            title="Page not found | robots.txt parser",
            form="form",
            error="404",
            canonical="/",
        ),
        404,
    )


@app.errorhandler(405)
def disallowed_method(error):
    return (
        render_template(
            "base.html",
            title="Submit the form to get parsed results | robots.txt parser",
            form="form",
            error="405",
            canonical="/",
        ),
        405,
    )
