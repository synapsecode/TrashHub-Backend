from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from TrashHubBackend.config import Config
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	CORS(app)

	#Import all your blueprints
	from TrashHubBackend.main.routes import main
	
	#use the url_prefix arguement if you need prefixes for the routes in the blueprint
	app.register_blueprint(main)

	return app

#Helper function to create database file directly from terminal
def create_database():
	import TrashHubBackend.models
	print("Creating App & Database")
	app = create_app()
	with app.app_context():
		db.create_all()
		db.session.commit()
	print("Successfully Created Database")
