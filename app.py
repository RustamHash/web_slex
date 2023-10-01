from flask import Flask, render_template, url_for, redirect, flash, request, g, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3
import os

from werkzeug.security import check_password_hash, generate_password_hash

from models.forms import LoginForm
from models.UserLogin import UserLogin
from models.FDataBase import FDataBase

# конфигурация
DATABASE = '/static/sql/vl_db.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'vl_db.db')))
login_manager = LoginManager(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sql_command.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
@login_required
def main():
    if current_user.is_authenticated:
        return redirect(url_for('index', username_url=current_user.get_login()))


@app.route('/<username_url>', methods=['GET', 'POST'])
@login_required
def index(username_url):
    return render_template('index.html', title="Главная", menu = dbase.get_contracts())


@app.route('/<contract_url>/', methods=['POST', 'GET'])
def active_contract(contract_url):
    contract_title = request.args.get('contract_title')
    return render_template('index.html', title=contract_title, menu = dbase.get_contracts())

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = dbase.get_user_by_login(login_form.login.data)
        if user and check_password_hash(generate_password_hash(user['password']), login_form.password.data):
            user_login_var = UserLogin().create(user)
            rm = login_form.remember.data
            print(rm)
            login_user(user_login_var, remember=rm)
            return redirect(request.args.get("next") or url_for("index", username_url=current_user.get_login()))

        flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", title="Авторизация", form=login_form)


@app.route("/logout/")
def logout():
    flash(f"Пользователь: {current_user.get_login()} успешно вышел!", "success")
    logout_user()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run()
    # create_db()
