import os
from dotenv import load_dotenv
from pymongo import MongoClient
import json
import sys
from os.path import abspath
from os.path import dirname as d
parent_dir = f"{d(d(abspath(__file__)))}"
sys.path.append(f"{parent_dir}")
from data_hub.utils.database_ops import DashboardOps

def find_document(collection_name, document_id=None):
    load_dotenv()
    uri = os.getenv("PREF_DB_URI")
    db_name = os.getenv("PREF_DB_NAME")
    client = MongoClient(uri)
    db = client[db_name]

    try:
        # if not client:
        #     connect()

        collection = db[collection_name]
        # document_id = ObjectId(document_id)
        result = collection.find_one({'_id':document_id})
        # print(result)
        return result
    except Exception as e:
        print("Error:", e)
        return None
    
if __name__ == "__main__":
    doc = find_document("11", "11")
    preferences =  doc["preferences"]
    json_pref = json.loads(preferences)
    # print(json_pref)
    db = DashboardOps(user_id="11", preferences=json_pref)
    check_db = db.check_database_exists()
    if check_db:
        data = db.get_json_data()
        print(data)
        
    
    

