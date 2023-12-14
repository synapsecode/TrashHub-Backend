#Database Layer
from datetime import datetime
from typing import Dict
from sqlalchemy.ext.hybrid import hybrid_method
from TrashHubBackend import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	username = db.Column(db.String)
	password = db.Column(db.String)

	points = db.Column(db.Float, default=0.0)

	# Relationships
	RCXJobs = db.relationship('RCXJob', backref='client')
	

	def __repr__(self):
		return f"User({self.name}, {self.username})"
	
	def __init__(self, name, username, password):
		self.name = name
		self.username = username
		self.password = password

# ============================ (BinOcculars) ================================

class BinoccularDustbin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	type = db.Column(db.String)
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)

	def __repr__(self):
		return f"BinOccularDusbin({self.name}, {self.name}, ({self.lat}, {self.lng}))"
	
	def __init__( self, name='default', type='regular', lat=0.0, lng=0.0):
		self.name = str(name)
		self.type = str(type)
		self.lat = float(str(lat))
		self.lng = float(str(lng))

	def toJson(self) -> Dict:
		return {
			'name': self.name,
			'type': self.type,
			'lat': self.lat,
			'lng': self.lng,
		}
