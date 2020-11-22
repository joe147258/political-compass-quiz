import flask_login
from flask import Flask, render_template, request, redirect, url_for
from controller.quiz_controller import quiz_controller
from flask_login import LoginManager, UserMixin
from utilities import config, util

# App set up
login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
app.secret_key = 'key'

# Handles the quiz mappings and logic
app.register_blueprint(quiz_controller)

# Admin Page access
users = { config.admin_name():{'pw':config.admin_password()} }

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
        username = request.form.get('username')
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
    question_list = config.question_list()
    return render_template('admin.html', len = len(question_list), question_list = question_list)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'
  
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

