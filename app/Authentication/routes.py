from flask import render_template, flash, redirect, url_for
from . import authentication
from .forms import LoginForm, SignupForm

@authentication.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Handle login logic here
        flash('Login successful', 'success')
        return redirect(url_for('main.home'))
    return render_template('login.html', title='Login', form=form)

@authentication.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Handle signup logic here
        flash('Account created successfully', 'success')
        return redirect(url_for('authentication.login'))
    return render_template('signup.html', title='Sign Up', form=form)
