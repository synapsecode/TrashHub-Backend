from flask import render_template, request, Blueprint
ecoperks = Blueprint('ecoperks', __name__)

@ecoperks.route("/")
def ecoperks_home():
	return "This is the ecoperks module of TrashHubBackend"
