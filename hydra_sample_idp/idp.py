from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
import yaml
from hydra.resource import Resource
import hydra_sample_idp
import os.path

app = Flask(__name__)
app.secret_key = 'idp secret key'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

HYDRA_URL = 'http://localhost:4444'
CLIENT_ID = "idp-id"
CLIENT_SECRET = "idp-secret"
res = Resource(HYDRA_URL, CLIENT_ID, CLIENT_SECRET)


def _get_resouce_path(resource_name):
    return os.path.join(hydra_sample_idp, 'resource', resource_name)


def auth(name, password):
    with open(_get_resouce_path('id.yml')) as f:
        ids = yaml.load(f)
    for i in ids:
        if i['name'] == name and i['password'] == password:
            return True
    return False


def get_information(name):
    with open(_get_resouce_path('pi.yml')) as f:
        info = yaml.load(f)
    for i in info:
        if i['name'] == name:
            return i
    raise Exception('No data')


def get_information_all():
    with open(_get_resouce_path('pi.yml')) as f:
        info = yaml.load(f)
    return info


class User():
    def __init__(self, username, data=None):
        self.username = username
        self.data = data

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @classmethod
    def auth(cls, username, password):
        if auth(username, password):
            return User(username)
        return None


@login_manager.user_loader
def load_user(username):
    return User(username)


@app.route('/')
@login_required
def index():
    return 'IDPへようこそ, %sさん' % (current_user.username)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.auth(username, password)
        if user:
            login_user(user)
            return redirect(request.args.get('next', '/'))
#            return redirect(url_for('information', username=user.username))
        else:
            error = "ユーザID またはパスワードが違います"
            return render_template("login.html", username=username, password=password, error=error)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/information", methods=["GET"])
@login_required
def information():
    user = current_user.username
    try:
        information = get_information(user)
    except:
        information = "No Data"
    return jsonify(information)


@app.route("/information_use_token", methods=["GET"])
def information_use_token():
    token = request.args.get('token')
    try:
        result = res.introspect(token)
    except:
        return "Invalid token", 400
    print("@@@ introspect result", result)

    # トークンのvalidate
    if result and result['active'] and 'pi' in result['scope']:
        return jsonify(get_information_all())
    return "Invalid Token...", 400


@app.route("/api/auth", methods=["GET"])
def auth_api():
    # 認証のためのAPI(デバッグのため超簡単に作成)
    username = request.args.get("username")
    password = request.args.get("password")
    if auth(username, password):
        return "ok", 200
    else:
        return "failed", 400


def cli():
    app.run(host="0.0.0.0", port=65001)


if __name__ == "__main__":
    cli()
