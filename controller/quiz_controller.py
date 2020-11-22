from flask import Flask, render_template, request, redirect, Blueprint, url_for, jsonify
from utilities import util
from utilities import config

quiz_controller = Blueprint('quiz_controller', __name__, template_folder='templates')
# Constants that are used to ensure data
# coming from the form is valid.
CONST_ECONOMIC = ['left', 'right']
CONST_SOCIAL = ['lib', 'auth']

@quiz_controller.route('/')
def home():
    return render_template('main.html', config_json = config.config(), intro_text = config.intro_text());

@quiz_controller.route('/finish-quiz')
def finish():
    try:
        x_value = int(request.args.get('x'))
        y_value = int(request.args.get('y'))
    except:
        return redirect('/')

    if not util.valid_params(x_value, y_value):
        return redirect('/')

    util.manipulate_image(x_value, y_value)
    path = 'static/images/image{0}{1}.png'
    formattedPath = path.format(x_value, y_value)

    # Starts a thread and deleted the image after X seconds
    # X chosen in config.json
    util.delete_image(formattedPath)

    return render_template('result.html', compass_image = formattedPath)

@quiz_controller.route('/submit-question', methods=['POST'])
def submit_question():
    try:
        # Validates the data is correct and if so adds the question
        for key, val in request.form.items():
            if len(val) <=0 or val is None:
                raise Exception('Null or length 0.')

        sway = request.form['sway']
        question_type = request.form['type']
        question = request.form['question_text']

        if question_type == 'economic':
            if sway not in CONST_ECONOMIC:
                raise Exception('Invalid Values.')
        elif question_type == 'social':
            if sway not in CONST_SOCIAL:
                raise Exception('Invalid Values.')
        else:
            raise Exception('Invalid Values.')

        util.add_question(question, question_type, sway)

        resp = jsonify(success=True)
        
    except Exception as e:
        print(e)
        resp = jsonify(success=False)
    
    return resp
        