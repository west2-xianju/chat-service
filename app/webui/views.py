from flask import session, redirect, url_for, render_template, request
from app.webui import webui
from .forms import LoginForm
from app.utils import jwt_functions

@webui.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['token'] = jwt_functions.generate_jwt({'user_id': form.user_id.data, 'blocked': False})
        session['room_id'] = form.room_id.data
        return redirect(url_for('.chat'))

    return render_template('index.html', form=form)


@webui.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    payload = jwt_functions.verify_jwt(session.get('token', None))
    if not payload:
        return redirect(url_for('.index'))
    return render_template('chat.html', name=payload['user_id'], room=session['room_id'])
 