from flask import Flask, render_template, request, redirect, Blueprint, url_for
from utilities import util
from utilities import config

quiz_controller = Blueprint('quiz_controller', __name__, template_folder='templates')

@quiz_controller.route("/")
def home():
    return render_template("main.html", config_json = config.config(), intro_text = config.intro_text());

@quiz_controller.route("/finish-quiz")
def finish():
    try:
        x_value = int(request.args.get('x'))
        y_value = int(request.args.get('y'))
    except:
        return redirect("/")

    if not util.valid_params(x_value, y_value):
        return redirect("/")

    util.manipulate_image(x_value, y_value)
    path = "static/images/image{0}{1}.png"
    formattedPath = path.format(x_value, y_value)

    # Starts a thread and deleted the image after X seconds
    # X chosen in config.json
    util.delete_image(formattedPath)

    return render_template("result.html", compass_image = formattedPath)