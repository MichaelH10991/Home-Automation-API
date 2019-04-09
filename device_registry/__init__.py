import markdown
import os
import shelve

# import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# create an instance of flask
app = Flask(__name__)
api = Api(app)

def get_db():
        db = getattr(g, '_database', None)
        if db is None:
                db = g._database = shelve.open("devices.db")
        return db

@app.teardown_appcontext
def teardown_db(exception):
        db = getattr(g, '_database', None)
        if db is not None:
                db.close()

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to html
        return markdown.markdown(content)

class DeviceList(Resource):
        def get(self):
                shelf = get_db()
                keys = list(shelf.keys())
                devices = [shelf[key] for key in keys]
                return {'message': 'Success', 'data': devices}

        def post(self):
                parser = reqparse.RequestParser()

                parser.add_argument('identifier', required=True)
                parser.add_argument('name', required=True)
                parser.add_argument('device_type', required=True)
                parser.add_argument('controller_gateway', required=True)

                #parse the arguments into an object
                args = parser.parse_args()
                shelf = get_db()
                shelf[args['identifier']] = args

                return {'message': 'Device registered', 'data': args}, 201

class Device(Resource):
        def get(self, identifier):
                shelf = get_db()

                #if the key does not exist in the datastore return a 404
                if not (identifier in shelf):
                        return {'message': 'Device not found', 'data': {}}, 404

                return {'message': 'Device found', 'data': shelf[identifier]}, 200

        def delete(self, identifier):
                shelf = get_db()
                #if the key does not exist in the datastore return a 404
                if not (identifier in shelf):
                        return {'message': 'Device not found', 'data': {}}, 404
                
                del shelf[identifier]
                return '', 204

api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')


