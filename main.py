import flask_login
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from controller.quiz_controller import quiz_controller
from flask_login import LoginManager, UserMixin
from utilities import json_parser, util, service
import os

# Constants that are used to ensure data
# coming from the form is valid.
CONST_ECONOMIC = ['left', 'right']
CONST_SOCIAL = ['lib', 'auth']

# App set up
login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)
app.secret_key = 'key'

# Handles the quiz mappings and logic
app.register_blueprint(quiz_controller)

# Admin Page access
users = { json_parser.admin_name():{'pw':json_parser.admin_password()} }

class User(UserMixin):
  pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return 0

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username
    try:
        user.is_authenticated = util.hash_string(request.form['pw']) == users[username]['pw']
    except Exception:
        return redirect(url_for('login') + '?error=1')
    
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').lower()
        try:
            if util.hash_string(request.form.get('pw')) == users[username]['pw']:
                user = User()
                user.id = username
                flask_login.login_user(user)
                return redirect(url_for('admin'))
        except Exception:
            return redirect(url_for('login') + '?error=1')

    return render_template('login.html')

@app.route('/admin')
@flask_login.login_required
def admin():
    question_list = json_parser.question_list()
    return render_template('admin.html', len = len(question_list), question_list = question_list)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'
  
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/icons'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/submit-question', methods=['POST'])
@flask_login.login_required
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

        service.add_question(question, question_type, sway)
        
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    
    return "Success", 200

@app.route('/delete-question', methods=['POST'])
@flask_login.login_required
def delete_question():
    try:
        position = int(request.form['pos'])
        service.delete_question(position);
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    
    return "Success", 200

@app.route('/edit-question', methods=['POST'])
@flask_login.login_required
def edit_question():
    try:
        print(int(request.form['pos']))
        print(request.form['form'])
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    
    return "Success", 200

@app.route('/get-question-info', methods=['GET'])
def get_question_info():
    try:
        pos = int(request.args.get('pos'))
        data = service.question_info(pos)
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    return data

if __name__ == '__main__':
    app.run(debug=True)