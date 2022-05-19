from flask import render_template, redirect, session, request, flash
from flask_app import app
import requests




@app.route("/players_weapons")
def store():
    headers = { 
        'TRN-api-key': 'd24c19bf-7b49-480b-9aa9-3752c5016253' #this is where we pass the headers
    }
    r = requests.get('https://api.fortnitetracker.com/v1/store', headers=headers)
    return render_template("store.html", items = r.json()) #store.html is going to take all the items in the r.json 