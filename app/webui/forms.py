from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    user_id = StringField('user_id', validators=[DataRequired()])
    room_id = StringField('room_id', validators=[DataRequired()])
    submit = SubmitField('Enter Chatroom')
