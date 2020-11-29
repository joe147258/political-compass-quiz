from flask import Flask, render_template, request, redirect, Blueprint, url_for, jsonify
from utilities import util, JsonReadWrite, service

quiz_controller = Blueprint('quiz_controller', __name__, template_folder='templates')

@quiz_controller.route('/')
def home():
    return render_template('main.html', config_json = JsonReadWrite.config(), intro_text = JsonReadWrite.intro_text(), 
                            question_list = JsonReadWrite.question_list(), project_text = JsonReadWrite.project_text());

@quiz_controller.route('/layout')
def layout():
    return render_template('layout.html');

@quiz_controller.route('/finish-quiz')
def finish():
    try:
        x_value = int(request.args.get('x'))
        y_value = int(request.args.get('y'))
    except:
        return redirect('/')

    if not util.valid_params(x_value, y_value):
        return redirect('/')

    # To ensure they stay within the boundries
    if x_value > 485:
        x_value = 485

    if x_value < 15:
        x_value = 15

    if y_value < 35:
        y_value = 35

    if y_value > 505:
        y_value = 505

    title = util.determine_ideology_title(x_value, y_value)
    util.manipulate_image(x_value, y_value)
    path = 'static/images/image{0}{1}.png'
    formattedPath = path.format(x_value, y_value)

    # Starts a thread and deleted the image after X seconds
    # X chosen in config.json
    util.delete_image(formattedPath)

    return render_template('result.html', compass_image = formattedPath, ideology = title)

@quiz_controller.route('/get-question-info', methods=['GET'])
def get_question_info():
    try:
        pos = int(request.args.get('pos'))
        data = service.question_info(pos)
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    return data
        