from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from TrashHubBackend.config import Config
from flask_cors import CORS
from flask_qrcode import QRcode


db = SQLAlchemy()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	CORS(app)
	QRcode(app)
	app._static_folder = Config().UPLOAD_FOLDER

	#Import all your blueprints
	from TrashHubBackend.main.routes import main
	from TrashHubBackend.user.routes import user
	from TrashHubBackend.recyclehub.routes import recyclehub
	from TrashHubBackend.ecoperks.routes import ecoperks
	
	#use the url_prefix arguement if you need prefixes for the routes in the blueprint
	app.register_blueprint(main)
	app.register_blueprint(user, url_prefix='/user')
	app.register_blueprint(recyclehub, url_prefix='/recyclehub')
	app.register_blueprint(ecoperks, url_prefix='/ecoperks')

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
