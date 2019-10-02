from threading import Lock

from pymongo import MongoClient


class Database:
    db = None
    instance = None
    lock = Lock()

    def __init__(self, online):

        if online:
            MONGODB_URI = "mongodb+srv://admin:admin@bdio-tbos5.gcp.mongodb.net/test?retryWrites=true&w=majority"
            client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
            self.db = client.get_database("BDIO")
        else:
            client = MongoClient('localhost', 27017)
            self.db = client.Censys

    @staticmethod
    def get_instance(online):
        Database.lock.acquire()

        if Database.instance is None:
            Database.instance = Database(online)
        Database.lock.release()

        return Database.instance


# Database Connection Online
db = Database.get_instance(online=True).db
