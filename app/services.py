from flask import Flask, render_template, request
import requests as r
from .models import Pokemon, db




def findpokemon(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    response = r.get(url)
    if response.ok:
        my_dict = response.json()
        pokemon_dict = {}
        pokemon_dict["Name"] = my_dict["name"]
        pokemon_dict["Ability"] = my_dict["abilities"][0]["ability"]["name"]
        pokemon_dict["Front_Shiny"] = my_dict["sprites"]["front_shiny"]
        pokemon_dict["Base_ATK"] = my_dict["stats"][1]["base_stat"]
        pokemon_dict["Base_HP"] = my_dict["stats"][0]["base_stat"]
        pokemon_dict["Base_DEF"] = my_dict["stats"][2]["base_stat"]
        return pokemon_dict
    else:
        raise Exception("The pokemon you're looking for does not exist.")



# def catch_pokemon(pokemon_name, user_id):
#     existing_pokemon = db.session.query(Pokemon).filter_by(name=pokemon_name).first()
#     if existing_pokemon:
#         print(f"{pokemon_name} already exists in the database.")
#         # check if the user already has this pokemon in their collection
#         if existing_pokemon.user_id == user_id:
#             print(f"{pokemon_name} is already in your pokedex.")
#         # check if the user has less than 5 total pokemon
#         elif db.session.query(Pokemon).filter_by(user_id=user_id).count() < 5:
#             existing_pokemon.user_id = user_id
#             db.session.commit()
#             print(f"{pokemon_name} has been added to your pokedex.")
#         else:
#             print("You already have 5 Pokemon in your pokedex.")
#     else:
#         # create new pokemon and add to the user's collection
#         new_pokemon = Pokemon(name=pokemon_name, user_id=user_id)
#         db.session.add(new_pokemon)
#         db.session.commit()
#         print(f"{pokemon_name} has been added to your collection.")