from flask import render_template, request, Blueprint
recyclehub = Blueprint('recyclehub', __name__)

@recyclehub.route("/")
def recyclehub_home():
	return "This is the recyclehub module of TrashHubBackend"
