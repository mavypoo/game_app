from dataclasses import dataclass
from flask_app import app
from flask import render_template, redirect, request, session, flash
# Import your models
from flask_app.models import user, game
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

#add_game_form
@app.route("/new/game")
def add_game_page():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("add_game.html", user = user.User.get_by_id(data))

#add_game_db
@app.route("/games/add_to_db", methods=["POST"])
def add_game_to_database():
    if "user_id" not in session:
        return redirect("/")
    if not game.Game.validate_game(request.form):
        return redirect("/new/game")
    data = {
        "name": request.form["name"],
        "genre": request.form["genre"],
        "subgenre": request.form["subgenre"],
        "max_players": request.form["max_players"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    game.Game.add_game(data)
    return redirect("/dashboard")

#view_game_db
@app.route("/show/<int:id>")
def view_one_game_page(id):
    if "user_id" not in session:
        return redirect("/")
    game_data = {
        "id": id,
    }
    return render_template("view_game.html", this_game = game.Game.get_one_game_with_user(game_data))


#edit_game_form
@app.route("/edit/<int:id>")
def edit_game_page(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    return render_template("edit_game.html", user = user.User.get_by_id(data), this_game = game.Game.get_one_game_with_user(data))

#edit_game_db
@app.route("/game/<int:id>/edit_in_db", methods=["POST"])
def edit_game_to_database(id):
    if "user_id" not in session:
        return redirect("/")
    if not game.Game.validate_game(request.form):
        return redirect(f"/edit/{id}")
    data = {
        "name": request.form["name"],
        "genre": request.form["genre"],
        "subgenre": request.form["subgenre"],
        "max_players": request.form["max_players"],
        "description": request.form["description"],
        "id": id, 
    }
    game.Game.edit_game(data)
    return redirect('/dashboard')

@app.route("/games/<int:id>/delete")
def delete_game(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id, 
    }
    game.Game.delete_game(data)
    return redirect("/dashboard")

