from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import app
from flask import flash
from flask_app.models import user


class Game: 
    db = "game_app"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.genre = data["genre"]
        self.subgenre = data["subgenre"]
        self.max_players = data["max_players"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None 

    #add to the db
    @classmethod 
    def add_game(cls, data): 
        query = "INSERT INTO games (name, genre, subgenre, max_players, description, user_id) VALUES (%(name)s, %(genre)s, %(subgenre)s, %(max_players)s, %(description)s, %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    #all games with users dashboard
    @classmethod
    def get_all_games_with_users(cls):
        query = "SELECT * FROM games JOIN users on users.id = games.user_id;"
        results = connectToMySQL(cls.db).query_db(query) 
        if len(results) < 1:
            return None
        else: 
            all_games = []
            for each_game in results:
                game_instance = cls(each_game)
                user_data = {
                    "id": each_game["users.id"],
                    "first_name": each_game["first_name"],
                    "last_name": each_game["last_name"],
                    "email": each_game["email"],
                    "password": each_game["password"],
                    "created_at": each_game["users.created_at"],
                    "updated_at": each_game["users.updated_at"]
                }
                game_creator = user.User(user_data)
                game_instance.user = game_creator
                all_games.append(game_instance)
            return all_games 

    @classmethod
    def get_one_game_with_user(cls, data):
        query = "SELECT * from games JOIN users on users.id = games.user_id WHERE games.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data) 
        if len(results) < 1:
            return None
        else: 
            one_game = cls(results[0])
            user_data = {
                "id": results[0]["users.id"],
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "email": results[0]["email"],
                "password": results[0]["password"],
                "created_at": results[0]["users.created_at"],
                "updated_at": results[0]["users.updated_at"],
            }
            game_creator = user.User(user_data)
            one_game.user = game_creator
            return one_game

    @classmethod
    def edit_game(cls, data):
        query = "UPDATE games SET name = %(name)s, genre = %(genre)s, subgenre = %(subgenre)s, max_players = %(max_players)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_game(cls, data):
        query = "DELETE FROM games WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_game(form_data):
        print(form_data)
        is_valid = True
        if len(form_data['name']) < 1:
            is_valid = False
            flash("All fields  required.")
        if len(form_data["genre"]) < 1:
            is_valid = False
            flash("All fields required.")
        if len(form_data["subgenre"]) < 1:
            is_valid = False
            flash("All fields required.")
        if form_data["max_players"] == '' or int(form_data['max_players']) < 1:
            is_valid = False
            flash("Number of max players must be 1 or more.")
        if len(form_data["description"]) < 1:
            is_valid = False
            flash("All fields required.")
        return is_valid
        