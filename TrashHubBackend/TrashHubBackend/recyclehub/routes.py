from flask import jsonify, render_template, request, Blueprint
from TrashHubBackend import db
from TrashHubBackend.models import RCXJob, RCXPartner, User
recyclehub = Blueprint('recyclehub', __name__)

@recyclehub.route("/")
def recyclehub_home():
	return "This is the recyclehub module of TrashTraceBackend"

@recyclehub.route("/partner/register", methods=['POST'])
def partner_register():
	data = request.json
	uname = data['username']
	name = data['name']
	type = data['type']
	password = data['password']
	if(None in [uname, name, password, type]):
		return "Invalid Payload", 400
	
	v = RCXPartner.query.filter_by(username=uname).first()
	if(v != None):
		return 'Partner already exists', 400
	
	v = RCXPartner(name=name, username=uname, password=password, type=type)
	db.session.add(v)
	db.session.commit()
	return 'Registered!'

@recyclehub.route('/partner/login', methods=['POST'])
def partner_login():
	data = request.json
	if(data == None or data == ''):
		return 'Invalid Request Body', 400
	v = RCXPartner.query.filter_by(username=data['username'], password=data['password']).first()
	if(v == None):
		return jsonify({
			'success': False,
			'message': 'Parner Not Found'
		})
	return jsonify({
		'success': True,
		'id': v.id
	})

@recyclehub.route("/partner/<pid>/alljobs")
def get_all_jobs(pid):
	p = RCXPartner.query.filter_by(id=pid).first()
	if(p == None):
		return 'Partner not Found'
	all_jobs = []
	for job in p.jobs:
		data = {
			'id': job.id,
			'name': job.name,
			'status': job.status,
			'date': job.date,
			'destination': [job.lat, job.lng],
			'client_name': job.client.name
		}
		all_jobs.append(data)
	return jsonify(all_jobs)

@recyclehub.route('/partner/update_job_status', methods=['POST'])
def update_job_status():
	#TODO: Add Partner Specific Updation Ability
	data = request.json
	if(data == None or data == ''):
		return 'Invalid Request Body', 400
	jid = data['job_id']
	status = data['status']
	j = RCXJob.query.filter_by(id=jid).first()
	if(j == None):
		return 'Job not found', 400
	
	j.status = status
	db.session.commit()

	return 'Status Updated', 200

# ===================================[ USER ]========================================

@recyclehub.route('/getpartners/<flt>')
def getpartners(flt):
	partners = None
	if(flt == 'all'):
		partners = RCXPartner.query.all()
	else:
		partners = RCXPartner.query.filter_by(type=flt).all()
	
	if(partners == None):
		return 'Invalid Filter', 400
	px = []
	for partner in partners:
		px.append({
			'id': partner.id,
			'name': partner.name,
			'type': partner.type,
		})
	return jsonify(px)


@recyclehub.route('/book_job', methods=['POST'])
def book_job():
	data = request.json
	if(data == None or data == ''):
		return 'Invalid Request Body', 400
	name = data['name']
	status = data['status']
	lat = data['destination']['lat']
	lng = data['destination']['lng']
	uid = data['user_id']
	pid = data['partner_id']

	if(None in [name, status, lat, lng, uid, pid]):
		return 'Invalid Payload', 400

	u = User.query.filter_by(id=uid).first()
	if(u == None):
		return 'No User Found', 400
	
	p = RCXPartner.query.filter_by(id=pid).first()
	if(u == None):
		return 'No Partner Found', 400

	j = RCXJob(name=name, status=status,lat=lat,lng=lng,client=u, partner=p)
	db.session.add(j)
	db.session.commit()

	return jsonify({
		'success': True,
		'id': j.id
	})

@recyclehub.route('/myjobs/<uid>')
def get_my_jobs(uid):
	u = User.query.filter_by(id=uid).first()
	if(u == None):
		return 'No User Found', 400
	jobs = RCXJob.query.filter_by(client=u).all()
	jbs = []
	
	for j in jobs:
		jbs.append({
			'name': j.name,
			'status': j.status,
			'date': j.date,
			'partner': {
				'name': j.partner.name,
				'type': j.partner.type,
			}
		})
	
	return jsonify(jbs)
	
