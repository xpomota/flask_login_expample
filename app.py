import flask
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'MY SECRET KEY'

login_manager = LoginManager()

login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, login, password):
        self.id = login
        self.password = password

USERS = {
    'admin': User('admin', 'adminpwd'),
 
}


class LoginForm(FlaskForm):
    login = StringField(
        'Логин',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 128)],
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 128)],
    )
    submit = SubmitField('Войти')


@login_manager.user_loader
def load_user(user_id):
    return USERS.get(user_id)


def check_user(user):
    user_in_list = USERS.get(user.id)
    if user_in_list and user_in_list.password == user.password:
        return user_in_list

    return None


# @app.route('/')
def index():
    return flask.render_template('index.html')
app.add_url_rule('/', view_func=index)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if user := check_user(User(form.login.data, form.password.data)):
            login_user(user)

        return flask.redirect(flask.url_for('index'))

    return flask.render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect('/')