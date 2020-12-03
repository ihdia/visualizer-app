from flask import Flask,send_file
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Images(Resource):
    
    def get(self):
        filename = "../../images/ASR/B02-S10-173.jpg"
        return send_file(filename,mimetype='image/gif')

api.add_resource(Images,'/images')

if __name__ == '__main__':
    app.run() 