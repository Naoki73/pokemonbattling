from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class AttackForm(FlaskForm):
    Attacker = StringField("Attacker", validators=[DataRequired()], render_kw={'autofocus': True})
    Opponent = StringField("Opponent", validators=[DataRequired()])
    submit = SubmitField()
    
class UserAttackForm(FlaskForm):
    opponent = StringField("Opponent username", validators=[DataRequired()], render_kw={'autofocus': True})
    submit_user = SubmitField()
    

# class AddPokemonForm(FlaskForm):
#     name = StringField('Name')
#     submit = SubmitField('Catch Pokemon')