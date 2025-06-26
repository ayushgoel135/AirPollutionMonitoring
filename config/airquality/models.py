from django.db import models
from pymongo import MongoClient
from config.settings import MONGO_URI, MONGO_DB_NAME
import json

class MongoDBConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance.client = MongoClient(MONGO_URI)
            cls._instance.db = cls._instance.client[MONGO_DB_NAME]
        return cls._instance
    
    def get_collection(self, collection_name):
        return self.db[collection_name]

class SatelliteData:
    @staticmethod
    def insert_data(data):
        mongo = MongoDBConnection()
        collection = mongo.get_collection('satellite_data')
        return collection.insert_one(data).inserted_id
    
    @staticmethod
    def get_all_data():
        mongo = MongoDBConnection()
        collection = mongo.get_collection('satellite_data')
        return list(collection.find({}))

class GroundMeasurement:
    @staticmethod
    def insert_data(data):
        mongo = MongoDBConnection()
        collection = mongo.get_collection('ground_measurements')
        return collection.insert_one(data).inserted_id
    
    @staticmethod
    def get_all_data():
        mongo = MongoDBConnection()
        collection = mongo.get_collection('ground_measurements')
        return list(collection.find({}))

class Prediction:
    @staticmethod
    def insert_data(data):
        mongo = MongoDBConnection()
        collection = mongo.get_collection('predictions')
        return collection.insert_one(data).inserted_id
    
    @staticmethod
    def get_all_data():
        mongo = MongoDBConnection()
        collection = mongo.get_collection('predictions')
        return list(collection.find({}))
    
    @staticmethod
    def get_latest_predictions(limit=100):
        mongo = MongoDBConnection()
        collection = mongo.get_collection('predictions')
        return list(collection.find({}).sort('timestamp', -1).limit(limit))