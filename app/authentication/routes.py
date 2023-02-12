from flask import Blueprint, redirect, url_for, render_template, request
from ..models import User
from .forms import SignupForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user



auth = Blueprint('auth', __name__, template_folder = 'auth-templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
    
            username = form.username.data
            email = form.email.data
            password = form.password.data

            print(username, email, password)


            user = User( username, email, password)
            print(user)

            user.saveToDB()

            return redirect(url_for('auth.login'))


    return render_template('signup.html', form=form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    login_user(user)
                    print('Log in successful!')
                    return redirect(url_for('index'))

                else:
                    print("Incorrect password")
            else: 
                print('User does not exist')
    return render_template('login.html', form=form)


@auth.route('/logout', methods=["GET"])
@login_required
def logoutRoute():
    logout_user()
    return redirect(url_for('auth.login'))

# @auth.route("/catch_pokemon", methods=["POST"])
# @login_required
# def catch_pokemon_route():
#     pokemon_name = request.form["pokemon_name"]
#     user_id = current_user.id
#     catch_pokemon(pokemon_name, user_id)
#     return redirect(url_for("home"))

# @auth.route('/profile')
# @login_required
# def profile():
#     user_id = current_user.id
#     collection = User.query.filter_by(id=user_id).first().pokemons
#     return render_template('profile.html', collection=collection)



