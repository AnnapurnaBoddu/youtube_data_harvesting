from pymongo import MongoClient
from data_extract import channel_details

def mongodb_data(data):
    """
    This function insert data into mongo db
    :param data:
    :return: inserted id
    """
    client = MongoClient('mongodb://localhost:27017/')

    # Access or create a database
    db = client['youtube']
    collections = db.list_collection_names()

    # Access or create a collection within the database
    channel_name = data['channel_name']['channel_name']
    if channel_name in collections:
        return 'Channel already exist in mongo db'
    else:
        collection = db[channel_name]
        # Insert the data into the collection
        result = collection.insert_one(data)
        return f'inserted documented id {result.inserted_id}'

    # Print the inserted document's ID
    #print("Inserted document ID:", result.inserted_id)

def mongodb_collection_names():
    """
    This function gives the list of collection names in mongo db
    :return: list of collection names
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['youtube']
    collection_names = db.list_collection_names()
    return collection_names


