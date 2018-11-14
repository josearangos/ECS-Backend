from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')


def connect():
    # Establish connection
    # print(config['MONGODB']['MONGO_URL'])
    #client = MongoClient(config['MONGODB']['MONGO_URL'])
    uri = config['MONGODB']['ConnectionString']
    client = MongoClient(uri)
    # Get the database
    db = client.census_database_v1

    #db.authenticate(name=config['MONGODB']['MONGO_USERNAME'], password=config['MONGODB']['MONGO_USERNAME'])
    return db


def connectCensusNight():
    # Establish connection
    # print(config['MONGODB']['MONGO_URL'])
    #client = MongoClient(config['MONGODB']['MONGO_URL'])
    uri = config['MONGODB']['ConnectionStringCensusNight']
    client = MongoClient(uri)
    # Get the database
    db_CN = client.db_census_night
    #db.authenticate(name=config['MONGODB']['MONGO_USERNAME'], password=config['MONGODB']['MONGO_USERNAME'])
    return db_CN


def migrar_Bd_Other_Server():
    client = MongoClient("mongodb://localhost:27017/")
    client.admin.command('copydb',
                         fromdb='census_database_v1',
                         todb='census_database_v1',
                         fromhost='mongodb://adminECS:adminECS12345@ds151970.mlab.com:51970/census_database_v1')
