from TrashHubBackend import create_app, db
from TrashHubBackend.models import User, BinoccularDustbin

class BinOccularMigrations:
    def migrate(self, json):
        print('Migrating Bins from Provided Json Data')
        bins = []
        for b in json:
            o = BinoccularDustbin(
                lat= b['lat'],
                lng= b['lng'],
                name= b['name'],
                type= b['type']
            )
            bins.append(o)
        app = create_app()
        with app.app_context():
            db.session.bulk_save_objects(bins)
            db.session.commit()
        print('Done Migrating')
          


bindata = [
  {
    "lat": 12.925198627442173,
    "lng": 77.58833301168083,
    "name": "Ample Mart",
    "type": "Biodegradable"
  },
  {
    "lat": 12.924513097966447,
    "lng": 77.58711438291554,
    "name": "Old Paper Shop",
    "type": "Recyclable"
  },
  {
    "lat": 12.924771350391909,
    "lng": 77.58586528324886,
    "name": "Bolas",
    "type": "Non-Biodegradable"
  },
  {
    "lat": 12.921769360587382,
    "lng": 77.58948515574994,
    "name": "Brindavan Garden",
    "type": "Biodegradable"
  },
  {
    "lat": 12.921132461990384,
    "lng": 77.58509359768375,
    "name": "Shalini Grounds",
    "type": "Non-Biodegradable"
  },
  {
    "lat": 12.907811256950685,
    "lng": 77.56612698918318,
    "name": "DSCE CS Block",
    "type": "MAMT"
  },
  {
    "lat": 12.908972036881718,
    "lng": 77.56650975218474,
    "name": "DSCE Heritage Block",
    "type": "MAMT"
  },
  {
    "lat": 12.9086014,
    "lng": 77.5649548,
    "name": "KS Layout Hazmat",
    "type": "Hazardous"
  },
  {
    "lat": 12.9094857,
    "lng": 77.5648643,
    "name": "KS Layout EWaste",
    "type": "E-Waste"
  },
  {
    "lat": 12.908284629110758,
    "lng": 77.57292877546571,
    "name": "JPMetro",
    "type": "MAMT"
  },
  {
    "lat": 12.90338817949067,
    "lng": 77.5512121938089,
    "name": "DoreKere",
    "type": "MAMT"
  },
  {
    "lat": 12.9158938535868,
    "lng": 77.57355786376205,
    "name": "BSKMetro",
    "type": "MAMT"
  },
  {
    "lat": 51.50299863875462,
    "lng": -0.1412452138070443,
    "name": "BritishEmpire",
    "type": "MAMT"
  }
]




BinOccularMigrations().migrate(bindata)



