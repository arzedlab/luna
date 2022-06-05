from flask import render_template, request, redirect, flash, url_for
from .blueprint import auth
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user
from flask_login import login_required, current_user

@auth.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        from models import User

        if request.method == 'GET':
            return render_template('auth/login.html')
        elif request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

            print(email, password)
            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

            # if the above check passes, then we know the user has the right credentials
            login_user(user, remember=True)
            return redirect(url_for('auth.profile'))
    else:
        return redirect(url_for('auth.profile'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    elif request.method == 'POST':
        from models import User
        from app import db
        email = request.form.get('email')
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        username = User.query.filter_by(username=username).first()

        if username: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Username address already exists')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, username=username, role='user', password=password)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    else: 
        return "Wrong Request"


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    if current_user.role.lower() == 'admin':
        check_admin = True
        return render_template('auth/profile.html', name=current_user.name)
    else:
        return render_template('auth/profile.html', name=current_user.name)


