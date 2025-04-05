from flask import Flask
from flask_cors import CORS 

from backend.blueprints.author_blueprint import author_blueprint
from backend.blueprints.book_blueprint import book_blueprint

app = Flask(__name__)


app.register_blueprint(author_blueprint)
app.register_blueprint(book_blueprint)

CORS(app)

if __name__ == "__main__":
    app.run(debug=True)