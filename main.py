import flask_login
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from controller.quiz_controller import quiz_controller
from flask_login import LoginManager, UserMixin
from utilities import json_manager, util, service, universal_constants as const, cache_manager
import os

# App set up
login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)
app.secret_key = 'key'

# Handles the quiz mappings and logic
app.register_blueprint(quiz_controller)

# Admin Page access set up 
users = { json_manager.admin_name():{'pw':json_manager.admin_password()} }

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
    question_list = json_manager.question_list()
    return render_template('admin.html', len = len(question_list), question_list = question_list, 
                            undo_amount = len(cache_manager.undo_queue), redo_amount = len(cache_manager.redo_queue))

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
    try:
        form_items = request.form
        if util.validate_form_data(form_items):
            service.add_question(form_items)
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    
    return "Success", 200

@app.route('/delete-question', methods=['POST'])
@flask_login.login_required
def delete_question():
    try:
        pos = int(request.form['pos'])
        cache_manager.cache_action(const.DELETE_CONST, int(pos))
        service.delete_question(pos)
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    return_dict = {
        "undo_amount": len(cache_manager.undo_queue)
    }
    return return_dict, 200

@app.route('/edit-question', methods=['POST'])
@flask_login.login_required
def edit_question():
    try:
        form_items = request.form
        if util.validate_form_data(form_items):
            cache_manager.cache_action(const.EDIT_CONST, int(form_items['pos']))
            service.edit_question(form_items)
    except Exception as e:
        print(e)
        return "Invalid Request", 400
    return_dict = {
        "undo_amount": len(cache_manager.undo_queue)
    }
    return return_dict, 200

@app.route('/undo', methods=['POST'])
@flask_login.login_required
def undo():
    try:
        cache_manager.restore_undo()    
    except Exception as e:
        print(e)
        return "No Cache", 400
    return_dict = {
        "undo_amount": len(cache_manager.undo_queue),
        "redo_amount": len(cache_manager.redo_queue)
    }
    return return_dict, 200

@app.route('/redo', methods=['POST'])
@flask_login.login_required
def redo():
    try:
        cache_manager.restore_redo()    
    except Exception as e:
        print(e)
        return "No Cache", 400
    return_dict = {
        "undo_amount": len(cache_manager.undo_queue),
        "redo_amount": len(cache_manager.redo_queue)
    }
    return return_dict, 200

if __name__ == '__main__':
    app.run(debug=True)