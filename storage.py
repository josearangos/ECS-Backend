from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

def connect():
    # Establish connection
    #print(config['MONGODB']['MONGO_URL'])
    #client = MongoClient(config['MONGODB']['MONGO_URL'])
    uri = config['MONGODB']['ConnectionString']
    client = MongoClient(uri)
    # Get the database
    db = client.census_database_v1
    #db.authenticate(name=config['MONGODB']['MONGO_USERNAME'], password=config['MONGODB']['MONGO_USERNAME'])
    return db
