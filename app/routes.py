from flask import Flask, redirect, url_for, render_template, request, jsonify
import requests as r
from app import app
from app.services import findpokemon
from .models import Pokemon, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pokemon', methods=["GET", "POST"])
def pokemon():
    # addpokemon = Pokemon()
    print(request.method)
    if request.method == "POST":
        pokemon_name = request.form['name']
        pokemon_data = Pokemon.query.filter(Pokemon.name == pokemon_name).first()
        print(pokemon_data)
        if pokemon_data:
            return render_template("pokemon_data.html", pokemon_data = pokemon_data)
        pokemon_data = findpokemon(pokemon_name)
        print("line 25")

        # my_pokemon = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()
        new_pokemon = Pokemon(pokemon_data["name"], pokemon_data["Ability"], pokemon_data["Front_Shiny"],
                              pokemon_data["Base_ATK"], pokemon_data["Base_HP"], pokemon_data["Base_DEF"], current_user.id)

        new_pokemon.saveToDB()
        return render_template("pokemon_data.html", pokemon_data = pokemon_data)
    # else:
    #     return render_template("pokemon.html")

        # if request.form.get('catch'):
        #     if len(my_pokemon)+1 <= 5:
        #         new_pokemon = Pokemon(pokemon_data["Name"], pokemon_data["Ability"], pokemon_data["Front_Shiny"], pokemon_data["Base_ATK"], pokemon_data["Base_HP"], pokemon_data["Base_DEF"], current_user.id)

        #         new_pokemon.saveToDB()

        #         pokemon = Pokemon.query.filter_by(name=pokemon_name).first()

        #         current_user.catch_pokemon(pokemon)

        #     else:
        #         print("You cannot catch more pokemon")
        #         pass
        # return render_template("pokemon_data.html", pokemon_data = pokemon_data)

    # else:
    #     return render_template("pokemon.html")

    # else:
    return render_template("pokemon.html")


@app.route("/profile")
@login_required
def profile():
    my_pokemon = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()
    # pokedex_entries = user_pokedex.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", my_pokemon=my_pokemon)


@app.route("/catch_pokemon/<name>", methods=["POST"])
@login_required
def add_to_pokedex(name):
    pokemon = Pokemon.query.filter(Pokemon.name == name).first()
    print("test")

    my_pokemon = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()

    if len(my_pokemon)+1 <= 5:
        current_user.catch_pokemon(pokemon)
        #flash statement 'pokemon caught'
        return redirect(url_for('profile'))

    else:
        print("You cannot catch more pokemon") #could make flash statement
        return redirect(url_for('profile'))

    # pokemon = Pokemon.query.filter_by(pokemon_name).first()
    # current_user.catch_pokemon(pokemon)

    # pokemon_entry = Pokedex(id=current_user.id, pokemon_id=pokemon.pokemon_id)
    # pokemon_entry.saveToDB()
    pass


# @app.route("/profile")
# @login_required
# def profile():
#     my_pokemon = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()
#     # pokedex_entries = user_pokedex.query.filter_by(user_id=current_user.id).all()
#     return render_template("profile.html", my_pokemon = my_pokemon)

@app.route('/pokemon/<int:pokemon_id>/delete', methods=["GET"])
def deletePokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)

    pokemon.deleteFromDB()

    return redirect(url_for('profile'))
