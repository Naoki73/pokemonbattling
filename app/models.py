from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


#Come up with my idea of how I want my model to work to begin with, and make it simple

#Watch shoha's lecture on join tables
db = SQLAlchemy()


def load_user(id):
    return User.query.get(int(id))

user_pokedex = db.Table(
    "user_pokedex",
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.pokemon_id'), nullable=False)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    pokemon = db.relationship("Pokemon", 
        secondary = user_pokedex, 
        backref=db.backref("trainer", lazy="dynamic"), 
        lazy = 'dynamic'
        )
    

    #pokedex = db.relationship("Pokedex", lazy=True)
    # pokemon = db.relationship("Pokemon", secondary = user_pokedex, backref="user_pokedex", lazy=True)
    
   

    def __init__(self, username,  email, password):
        self.username = username
        self.email = email
        self.password = password

    

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def catch_pokemon(self, caught_pokemon):
        self.pokemon.append(caught_pokemon)
        db.session.commit()

    def see_my_pokemon(self):
        Show_pokemon = Pokemon.query.join(user_pokedex, (Pokemon.pokemon_id==user_pokedex.c.pokemon_id)).where(user_pokedex.c.user_id == self.id)
        # Show_pokemon = user_pokedex
        My_users_pokemon = Show_pokemon.union(self.pokemon)
        return My_users_pokemon

   


    

    
class Pokemon(db.Model):
    pokemon_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    Ability = db.Column(db.String(50), nullable=False)
    Front_Shiny = db.Column(db.String(200), nullable=False)
    Base_ATK = db.Column(db.Integer, nullable=False)
    Base_HP = db.Column(db.Integer, nullable=False)
    Base_DEF = db.Column(db.Integer, nullable=False)
    # Pokedex = db.relationship("Pokedex", lazy=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    



    def __init__(self, name, Ability, Front_Shiny, Base_ATK, Base_HP, Base_DEF):
        self.name = name
        self.Ability = Ability
        self.Front_Shiny = Front_Shiny
        self.Base_ATK = Base_ATK
        self.Base_HP = Base_HP
        self.Base_DEF = Base_DEF
        # self.user_id = user_id


    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()


# class Pokedex(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#     pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.pokemon_id'), nullable= False)
#     user = db.relationship("User", back_populates="pokedex")
#     pokemon = db.relationship("Pokemon", back_populates="pokedex")


#     def __init__(self, user_id, pokemon_id):
#         self.user_id = user_id
#         self.pokemon_id = pokemon_id

#     def saveToDB(self):
#         db.session.add(self)
#         db.session.commit()

#     def deleteFromDB(self):
#         db.session.delete(self)
#         db.session.commit()

#Remake pokedex join table 


# class Pokedex(db.Model):
#     pokedex_id = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     pokemon_id = db.Column (db.Integer, db.ForeignKey('pokemon.pokemon_id'), nullable= False)
#     User = db.relationship("User", lazy=True)
#     Pokemon = db.relationship("Pokemon", lazy=True)

#     def savetoDB(self):
#         db.session.add(self)
#         db.session.commit()
    