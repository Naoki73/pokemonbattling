from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class AttackForm(FlaskForm):
    Attacker = StringField("Attacker", validators=[DataRequired()], render_kw={'autofocus': True})
    Opponent = StringField("Opponent", validators=[DataRequired()])
    submit = SubmitField()
    
class UserAttackForm(FlaskForm):
    opponent = StringField("Opponent username", validators=[DataRequired()], render_kw={'autofocus': True})
    submit_user = SubmitField()
