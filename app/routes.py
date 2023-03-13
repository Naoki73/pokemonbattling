from random import randint

import requests as r
from app import app
from app.services import findpokemon
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user

from .models import Pokemon, User, user_pokedex
from .authentication.forms import AttackForm, UserAttackForm

#show all users at once, go to their own profile with like a profile/(otheruser) route function, then just battle from there


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
    
    return render_template("pokemon.html")


@app.route("/profile")
@login_required
def profile():
    
    my_pokemon = current_user.see_my_pokemon()
    
    return render_template("profile.html", my_pokemon=my_pokemon)


@app.route("/catch_pokemon/<name>", methods=["POST"])
@login_required
def add_to_pokedex(name):
    pokemon = Pokemon.query.filter(Pokemon.name == name).first()
    print("test")

    

    print(pokemon not in current_user.pokemon)
    print(current_user.pokemon.count())
    if current_user.pokemon.count() < 5 and pokemon not in current_user.pokemon:
        current_user.catch_pokemon(pokemon)

        message = flash("Pokemon caught!")
        return redirect(url_for('profile'))
    else:
        print("You cannot catch more pokemon")
        message = flash("You cannot catch more pokemon,", category="danger")
        return redirect(url_for('profile'))

   
    return render_template("pokemon.html")




@app.route('/pokemon/<int:pokemon_id>/delete', methods=["GET"])
def deletePokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    print(pokemon)
    current_user.delete_my_pokemon(pokemon)
    

    return redirect(url_for('profile'))

@app.route('/battle', methods=["GET", "POST"])
def battle():

    current_squad = []
    opponent_squad = []
    my_opponent = User.query.filter(User.id != current_user.id).first()



    for pokemon in current_user.pokemon:
        print(pokemon.name)
        dictionary = {}
        dictionary["name"] = pokemon.name
        dictionary["Ability"] = pokemon.Ability 
        dictionary["Front_Shiny"] = pokemon.Front_Shiny
        dictionary["Base_ATK"] = pokemon.Base_ATK
        dictionary["Base_HP"] = pokemon.Base_HP
        dictionary["Base_DEF"] = pokemon.Base_DEF
        current_squad.append(dictionary)

    # print(current_squad)

    for pokemon in my_opponent.pokemon:
        print(pokemon.name)
        dictionary = {}
        dictionary["name"] = pokemon.name
        dictionary["Ability"] = pokemon.Ability 
        dictionary["Front_Shiny"] = pokemon.Front_Shiny
        dictionary["Base_ATK"] = pokemon.Base_ATK
        dictionary["Base_HP"] = pokemon.Base_HP
        dictionary["Base_DEF"] = pokemon.Base_DEF
        opponent_squad.append(dictionary)

    # print(opponent_squad)


    for i in range(len(current_squad)):
        print(f"current_user.pokemon {current_squad[i]['name']}")
        print(f"opponent_user.pokemon {opponent_squad[i]['name']}")
        if current_squad[i]["Base_ATK"] > opponent_squad[i]["Base_ATK"]:
            print(f"{current_squad[i]['name']} is the winner!")
        else:
            print(f"{opponent_squad[i]['name']} is the winner!")



    form = AttackForm()
    opponentform = UserAttackForm()
    pokemons = Pokemon.query.filter_by(user_id = current_user.id)

    display_my_pokemon = current_user.see_my_pokemon()

    if request.method == "POST":

        if opponentform.validate():
            opponent_username = opponentform.opponent.data
            Opponent = User.query.filter_by(username = opponent_username).first()

            if Opponent:

                opponent_pokemons = Pokemon.query.join(User).filter(User.username == opponent_username).all()

                if form.validate():

                    attacker = form.attacker.data.capitalize()
                    opponent = form.opponent.data.capitalize()

                    cuserpokemon = Pokemon.query.filter_by(pokemon_name = attacker).first()
                    opponent_team = Pokemon.query.filter_by(pokemon_name = opponent).first()
                    return redirect(url_for('fight'))
                
                return render_template('battle.html',form = form, opponentform = opponentform, pokemons = pokemons, opponent_username = opponent_username, Opponent = Opponent, display_my_pokemon = display_my_pokemon, opponent_pokemons = opponent_pokemons)
            

            else:
                flash("No such user")
                return(redirect(url_for('battle')))
            

    return render_template('battle.html', form = form, opponentform = opponentform, pokemons = pokemons, display_my_pokemon = display_my_pokemon)

#have it go from /battle to /battle/<opponent_username> currently does not do that

@app.route('/battle/<opponent_username>', methods = ["GET", "POST"])
def fight(opponent_username):
    form = AttackForm()
    opponentform = UserAttackForm()
    opponentform.opponent.data = opponent_username
    pokemons = Pokemon.query.filter_by(user_id = current_user.id).all()
    # opponent_team = Pokemon.query.join(User).filter(User.username == opponent_username).all()
    opponent_pokemons = opponent_username.see_my_pokemon()
    # display_opponent_pokemon = current_user.see_my_pokemon()

    if request.method == "POST":
        if form.validate():
            attacker = form.attacker.data
            opponent = form.opponent.data

            cuserpokemon = Pokemon.query.filter_by(pokemon_name = attacker).first()
            opponent_team = Pokemon.query.filter_by(pokemon_name = opponent).first()

            if cuserpokemon not in pokemons:
                form.attacker.data = ''
                #return empty
            if opponent_team not in opponent_pokemons:
                form.opponent.data = ''


            #the attacking    
            if opponent_team in opponent_pokemons and cuserpokemon in pokemons:

                cuserpokemon.attack(opponent_team)
                opponent_pokemons = Pokemon.query.join(User).filter(User.username == opponent_username).all()
                pokemons = Pokemon.query.filter_by(user_id = current_user.id).all()


                if not opponent_team:
                    form.opponent.data = ''

                if opponent_pokemons:
                    if len(opponent_pokemons) > 1:
                        opponent_pokemons[randint(0, len(opponent_pokemons) -1)].attack(cuserpokemon)
                        #can perhaps make this just always start from the first pokemon on the list and append each pokemon that dies away to always make the remaining pokemon shift towards the start of the list 
                        pokemons = Pokemon.query.filter_by(user_id = current_user.id).all()
                        if not cuserpokemon:
                            form.attacker.data = ''

                    else:
                        opponent_pokemons[0].attack(cuserpokemon)
                        pokemons = Pokemon.query.filter_by(user_id == current_user.id).all()
                        #probably model command error above maybe

                else:
                    flash("You won!")
                    return redirect(url_for('index'))
                if not pokemons:
                    flash("You lose")
                    return redirect(url_for('homepage'))
                
            if not cuserpokemon:
                form.attacker.data = ''

            if not opponent_team:
                form.opponent.data = ''

            Opponent = User.query.filter_by(username = opponent_username).first()

            return render_template('battle.html', opponent_pokemons = opponent_pokemons, pokemons = pokemons, Opponent=Opponent, form = form)
        
        return render_template('battle.html', opponent_pokemons = opponent_pokemons, pokemons = pokemons, Opponent=Opponent, form = form)
    
    return render_template('battle.html', opponent_pokemons = opponent_pokemons, pokemons = pokemons, Opponent=Opponent, form = form)






    # my_pokemon = current_user.pokemon
    # other_user = User.query.get(user_id)
    # opponent = other_user.pokemon
    # users = User.query.all()

    # mine_alive = []
    # opps_alive = []

    # for pokemon in my_pokemon:
    #     mine_alive.append(pokemon)

    # for pokemon in opps_alive:
    #     opps_alive.append(pokemon)


    # A = 0
    # my_pokemon_wins = 0
    # opp_wins = 0

    # results = []

    # if len(my_pokemon) > len(opponent):
    #     while A < len(opponent):
    #         my_attack = my_pokemon[A].Base_ATK
    #         my_def = my_pokemon[A].Base_DEF
    #         my_health = my_pokemon[A].Base_HP
    #         opp_attack = opponent[A].Base_ATK
    #         opp_def = opponent[A].Base_DEF
    #         opp_health = opponent[A].Base_HP
    #         while True:
    #             attacker = ['my_pokemon', 'opponent']
    #             x = random.choice(attacker)
    #             print(x)
    #             if x == 'my_pokemon':
    #                 opp_def -= my_attack
    #                 if opp_def < 0:
    #                     opp_health += opp_def
    #                 if opp_health < 0:
    #                     results.append(current_user)
    #                     break
    #             else:
    #                 my_def -= opp_attack
    #                 if my_def < 0:
    #                     my_health += my_def
    #                 if my_health < 0:
    #                     results.append(other_user)
    #                     break
    #     print(results)

    #     A += 1
    #     continue

    # else:
    #     while A < len(my_pokemon):
    #         my_attack = my_pokemon[A].Base_ATK
    #         my_defense = my_pokemon[A].Base_DEF
    #         my_health = my_pokemon[A].Base_HP
    #         opp_attack = opponent[A].Base_ATK
    #         opp_def = opponent[A].Base_DEF
    #         opp_health = opponent[A].Base_HP
    #         while True:
    #             attacker = ['my_pokemon', 'opponent']
    #             x = random.choice(attacker)
    #             print(x)
    #             if x == 'my_pokemon':
    #                 opp_def -= my_attack
    #                 if opp_def < 0:
    #                     opp_health += opp_def
    #                 if opp_health < 0:
    #                     results.append(current_user)
    #                     break
    #             else:
    #                 my_def -= opp_attack
    #                 if my_def < 0:
    #                     my_health += my_defense



    return render_template("battle.html")
