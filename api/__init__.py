from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import os
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    
    db.init_app(app)


    from .views import main
    app.register_blueprint(main)
        
    if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=False, port=os.environ.get('PORT', 80))
    return app
