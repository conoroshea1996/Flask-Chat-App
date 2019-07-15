import os
from flask import Flask, redirect, render_template, request, session, url_for

from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SECRET', "randomstring123")
messages = []


def add_message(username, message):
    """ Add message to messages list """
    npw = datetime.now().strftime('%H:%M:%S')
    messages.append({'times': npw,
                     'from': username,
                     'message': message})


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page with insturctions """
    if request.method == 'POST':
        session['username'] = request.form['username']

    if 'username' in session:
        return redirect(url_for('user', username=session['username']))

    return render_template('index.html')


@app.route('/chat/<username>', methods=['GET', 'POST'])
def user(username):
    """ Display and Add  chat messages """
    if request.method == 'POST':
        username = session['username']
        message = request.form['message']
        add_message(username, message)
        return redirect(url_for('user', username=session['username']))

    return render_template('chat.html', username=username, chat_messages=messages)


app.run(host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '5000'), debug=False)
