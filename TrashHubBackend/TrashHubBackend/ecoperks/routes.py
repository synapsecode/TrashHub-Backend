from TrashHubBackend import db
from flask import render_template, request, Blueprint
from TrashHubBackend.models import (ProductBatch, ProductEntity,
				       TrashTagManufacturer, TrashTagProduct, 
					   TrashTagVendor, User)

ecoperks = Blueprint('ecoperks', __name__)

@ecoperks.route("/")
def ecoperks_home():
	return "This is the ecoperks module of TrashHubBackend"


# =============================== [ VENDOR ] =============================
@ecoperks.route("/vendor/register", methods=['POST'])
def vendor_register():
	data = request.json
	uname = data['username']
	name = data['name']
	password = data['password']
	if(None in [uname, name, password]):
		return "Invalid Payload", 400
	
	v = TrashTagVendor.query.filter_by(username=uname).first()
	if(v != None):
		return 'Vendor already exists', 400
	
	v = TrashTagVendor(name=name, username=uname, password=password)
	db.session.add(v)
	db.session.commit()
	return 'Registered!'

@ecoperks.route('/vendor/login', methods=['POST'])
def vendor_login():
	data = request.json
	if(data == None or data == ''):
		return 'Invalid Request Body', 400
	v = TrashTagVendor.query.filter_by(username=data['username'], password=data['password']).first()
	if(v == None):
		return jsonify({
			'success': False,
			'message': 'Vendor Not Found'
		})
	return jsonify({
		'success': True,
		'id': v.id
	})


@ecoperks.route("/vendor/scan", methods=['POST'])
def vendor_scan_qr():
	data = request.json
	qrcode = data['qrcode']
	vid = data['vid']
	if(qrcode == None or vid == None):
		return "Invalid Payload", 400
	v = TrashTagVendor.query.filter_by(id=vid).first()
	if(v == None):
		return "Invalid Vendor", 400
	bid, eid = qrcode.split(':') #batchid:entityid
	bat = ProductBatch.query.filter_by(id=bid).first()
	if(bat == None):
		return "Invalid Batch", 400
	ent = ProductEntity.query.filter_by(id=eid, batch=bat).first()
	if(ent == None):
		return "Invalid Entity", 400
	if(ent.purchased):
		return "Already Scanned", 400
	
	#Purchase the Entity
	ent.purchased = True

	#Award some points to vendor
	v.points = v.points + 5

	db.session.commit()

	return "Purchased", 200