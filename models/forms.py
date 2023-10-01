from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    login = StringField(render_kw={"placeholder": "Введите логин"}, validators=[DataRequired(), Length(min=4, max=10)])
    password = PasswordField(render_kw={"placeholder": "Введите пароль"}, validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField("Запомнить", default = True)
    submit = SubmitField("Войти")