from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.config.config import Config

app = Flask(__name__, template_folder='../templates')
app.secret_key = Config.SECRET_KEY
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    data['interests'] = request.form.getlist('interests')

    if not User.validate_user(data):
        return redirect('/')

    data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user_id = User.save(data)

    session['user_id'] = user_id
    return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    if not User.validate_login_email(email):
        return redirect('/')
    
    is_valid, user = User.validate_login(email, password)
    if not is_valid:
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/success')

from flask import redirect, render_template, session

@app.route('/success')
def success():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')

    user = User.get_by_id(user_id)
    if not user:
        return redirect('/')

    return render_template('success.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

