from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User ,db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
       
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logeed in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
               flash('wrong password', category='error')

        else:
            flash('user not found', category='error')       

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return  redirect('login')


@auth.route('/signup', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        frist_name=request.form.get('name')
        password = request.form.get('password')
        conPassword=request.form.get('password1')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already exist', category='error')
        elif len(email) < 4:
             flash('email is too short', category='error')
        elif len(frist_name) < 2:
             flash('name is too short', category='error')
        elif password != conPassword:
             flash('password dont match', category='error')
        elif len(password) < 7:
              flash('password is too short', category='error')
        else:
            #add user to database
          new_user = User(email=email, frist_name=frist_name, password=generate_password_hash(password))
          db.session.add(new_user)
          db.session.commit()
          login_user(new_user, remember=True)
          flash('account created!', category='success')
          return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)