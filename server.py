from flask_app import app
from flask_app.controllers  import users, games, stores

# Run the app here
if __name__=="__main__":
    app.run(debug=True)