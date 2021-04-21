from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['ParkingService']
col = db['Collection0']


def add_to_database(data):
    return col.insert_one(data).inserted_id


def get_from_database(elements, multiple=False):
    if multiple:
        results = col.find(elements)
        return [r for r in results]
    else:
        return col.find_one(elements)


def delete_from_database(element):
    col.delete_one(element)


def get_total_amount():
    pipeline = [{"$group": {"_id": "null", "total": {"$sum": "$amount"}}}]
    return list(col.aggregate(pipeline))