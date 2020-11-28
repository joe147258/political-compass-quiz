from flask import Flask, render_template, request, redirect, Blueprint, url_for, jsonify
from utilities import util
from utilities import json_parser

quiz_controller = Blueprint('quiz_controller', __name__, template_folder='templates')
# Constants that are used to ensure data
# coming from the form is valid.
CONST_ECONOMIC = ['left', 'right']
CONST_SOCIAL = ['lib', 'auth']

@quiz_controller.route('/')
def home():
    return render_template('main.html', config_json = json_parser.config(), intro_text = json_parser.intro_text(), question_list = json_parser.question_list());

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

    util.manipulate_image(x_value, y_value)
    path = 'static/images/image{0}{1}.png'
    formattedPath = path.format(x_value, y_value)

    # Starts a thread and deleted the image after X seconds
    # X chosen in config.json
    util.delete_image(formattedPath)

    return render_template('result.html', compass_image = formattedPath)

@quiz_controller.route('/submit-question', methods=['POST'])
def submit_question():
    sway = request.form['sway']
    question_type = request.form['type']
    question = request.form['question_text']
    try:
        # Validates the data is correct and if so adds the question
        for key, val in request.form.items():
            if len(val) <=0 or val is None:
                raise Exception('Null or length 0.')

        if question_type == 'economic':
            if sway not in CONST_ECONOMIC:
                raise Exception('Invalid Values.')
        elif question_type == 'social':
            if sway not in CONST_SOCIAL:
                raise Exception('Invalid Values.')
        else:
            raise Exception('Invalid Values.')

        util.add_question(question, question_type, sway)
        
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    
    return "Success", 200

@quiz_controller.route('/delete-question', methods=['POST'])
def delete_question():
    try:
        position = int(request.form['pos'])
        util.delete_question(position);
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    
    return "Success", 200
        