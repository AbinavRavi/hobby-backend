from dotenv import load_dotenv
import os
from data_hub.utils.log import logger
from data_hub.models.model import UserPreferences
from pymongo import MongoClient
import json
from typing import List
import psycopg2
from psycopg2 import sql


class MongoDataOps:
    def __init__(self, uri, db_name, collection_name) -> None:
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            return True
        except Exception as e:
            logger.error("Error:", e)
            return False

    def check_and_create_db(self, db_name) -> bool:
        if not self.client:
            self.connect()

        db_list = self.client.list_database_names()

        if db_name in db_list:
            logger.info(f"Database '{db_name}' already exists.")
        else:
            db = self.client[db_name]
            logger.info(f"Creating database '{db_name}'.")
            db.command("ping")
        return True

    def collection_exists_or_create(self, collection_name):
        try:
            if not self.client:
                self.connect()

            if collection_name in self.db.list_collection_names():
                logger.debug(f"Collection '{collection_name}' exists.")
            else:
                self.db.create_collection(collection_name)
                logger.info(f"Collection '{collection_name}' created.")

            return True
        except Exception as e:
            logger.error("Error:", e)
            return False

    def insert_data(self, data):
        try:
            self.db[self.collection_name].insert_one(data)
            logger.info(f"Data inserted into '{self.collection_name}'.")
            return True
        except Exception as e:
            logger.error("Error:", e)
            return False

    def update_data(self, query, new_data):
        try:
            self.db[self.collection_name].update_one(query, {"$set": new_data})
            logger.info(f"Data updated in '{self.collection_name}'.")
            return True
        except Exception as e:
            logger.error("Error:", e)
            return False

    def delete_data(self, query):
        try:
            self.db[self.collection_name].delete_one(query)
            logger.info(f"Data deleted from '{self.collection_name}'.")
            return True
        except Exception as e:
            logger.error("Error:", e)
            return False

    def read_data(self, query):
        try:
            data = self.db[self.collection_name].find_one(query)
            logger.info(f"Data read from '{self.collection_name}'.")
            return data
        except Exception as e:
            logger.error("Error:", e)
            return None

    def close_connection(self):
        if self.client:
            self.client.close()
            logger.info("Connection closed")


# class PreferencesDataOps(MongoDataOps):
#     def __init__(self, collection_name):
#         load_dotenv()
#         self.uri = os.getenv("PREF_DB_URI")
#         self.db_name = os.getenv("PREF_DB_NAME")
#         super().__init__(self.uri, self.db_name, collection_name)

#     def insert_document(self):
#         pass

#     def find_document(self):
#         pass

#     def update_document(self):
#         pass

#     def check_user(self, user_id):
#         if not self.client:
#             self.connect()

#         if user_id in self.db.list_collection_names():
#             return True
#         else:
#             return False


class PreferencesDataOps:
    def __init__(self):
        load_dotenv()
        self.uri = os.getenv("PREF_DB_URI")
        self.db_name = os.getenv("PREF_DB_NAME")
        self.username = os.getenv("PREF_DB_USERNAME")
        self.password = os.getenv("PREF_DB_PASSWORD")
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            return True
        except Exception as e:
            logger.error("Error:", e)
            return False

    def check_and_create_db(self, db_name) -> bool:
        if not self.client:
            self.connect()

        db_list = self.client.list_database_names()

        if db_name in db_list:
            logger.info(f"Database '{db_name}' already exists.")
        else:
            db = self.client[db_name]
            logger.info(f"Creating database '{db_name}'.")
            db.command("ping")
        return True

    def collection_exists_or_create(self, collection_name):
        try:
            if not self.client:
                self.connect()

            if collection_name in self.db.list_collection_names():
                logger.debug(f"Collection '{collection_name}' exists.")
            else:
                self.db.create_collection(collection_name)
                logger.info(f"Collection '{collection_name}' created.")

            return True
        except Exception as e:
            logger.error("Error:", e)
            return False

    def insert_document(self, collection_name, document, id):
        try:
            if not self.client:
                self.connect()
            insert_document = {"_id": id, "preferences": document}
            collection = self.db[collection_name]
            result = collection.insert_one(insert_document)
            logger.info("Document inserted with ID:", result.inserted_id)
            return True, result.inserted_id
        except Exception as e:
            logger.error("Error:", e)
            return False, None

    def find_document(self, collection_name, document_id=None):
        try:
            if not self.client:
                self.connect()

            collection = self.db[collection_name]
            # document_id = ObjectId(document_id)
            result = collection.find_one({"_id": document_id})

            return result
        except Exception as e:
            logger.error("Error:", e)
            return None

    def update_document(self, collection_name, query, document):
        try:
            if not self.client:
                self.connect()

            collection = self.db[collection_name]
            result = collection.update_one(query)
            logger.info(f"Updated the document - {result}")
            return True
        except Exception as e:
            logger.error("Error:", e)
            return False

    def check_user(self, user_id):
        if not self.client:
            self.connect()

        if user_id in self.db.list_collection_names():
            return True
        else:
            return False

    def close_connection(self):
        if self.client:
            self.client.close()
            logger.info("Connection closed")


class DashboardOps:
    def __init__(self, user_id, preferences):
        self.user_id = user_id
        self.preferences = preferences
        load_dotenv()
        self.host = os.getenv("MASTER_DB_HOST")
        self.port = os.getenv("MASTER_DB_PORT")
        self.dbname = os.getenv("MASTER_DB_NAME")
        self.user = os.getenv("MASTER_DB_USER")
        self.password = os.getenv("MASTER_DB_PASSWORD")
        self.table_name = os.getenv("MASTER_DB_TABLE_NAME")
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
            )
            return True
        except Exception as e:
            print("Error:", e)
            return False

    def check_database_exists(self):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()

        # Use the "information_schema" to check if the database exists
        query = sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;")
        cursor.execute(query, [self.dbname])

        # Fetch the result
        result = cursor.fetchone()
        if result[0] == 1:
            return True
        else:
            return False

    def read_filters(self):
        with open("data_hub/data/category_map.json") as f:
            category_map = json.load(f)
        return category_map

    def get_mapped_signals(self, signals: List):
        list_of_signals = []
        for signal in signals:
            list_of_signals.extend(self.read_filters()[signal])
        return list_of_signals

    def get_company_size(self, company_size: List):
        lowest = float("inf")  # Initialize lowest as positive infinity
        highest = float("-inf")  # Initialize highest as negative infinity

        for range_str in company_size:
            parts = range_str.split("-")

            if len(parts) == 2:
                # Extract the lowest and highest values
                try:
                    start = int(parts[0])
                    end = int(parts[1])
                    lowest = min(lowest, start)
                    highest = max(highest, end)
                except ValueError:
                    pass  # Ignore invalid range strings

        return lowest, highest

    def preferences_to_params(self):
        pref = UserPreferences.model_validate(self.preferences)
        geo = pref.preferences.geographies
        countries = ", ".join(country for country in geo)
        company_size = pref.preferences.company_size
        lowest_size, highest_size = self.get_company_size(company_size)
        signals = pref.preferences.signals
        all_signals = signals + ["basic_data"]
        mapped_signals = self.get_mapped_signals(all_signals)
        return mapped_signals, (countries, lowest_size, highest_size)

    def prepare_master_data_query(self, page, per_page):
        mapped_signals, query_params = self.preferences_to_params()
        signals_string = ", ".join(signal for signal in mapped_signals)
        offset = (page - 1) * per_page
        query = f"""
            SELECT {signals_string}
            FROM {self.table_name}
            WHERE hq_country = %s
            AND linkedin_headcount BETWEEN %s::int AND %s::int
            LIMIT {per_page}
            OFFSET {offset}
            """
        # AND linkedin_industries = %s;
        # """
        query_params = query_params
        return query, query_params

    def get_dataset_size(self, per_page=25):
        query, params = self.prepare_master_data_query(page=1, per_page=per_page)
        # Create a modified query to retrieve the total count without pagination
        count_query = f"SELECT COUNT(*) FROM ({query}) AS count_query"

        try:
            if not self.conn:
                self.connect()
            cursor = self.conn.cursor()
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0]
            cursor.close()

            # Calculate the total number of pages
            total_pages = (total_count + per_page - 1) // per_page
            return total_count, total_pages
        except Exception as e:
            logger.error("Error in getting total pages:", e)
            return None

    def get_master_data(self, page=1, per_page=25):
        query, params = self.prepare_master_data_query(page, per_page)
        try:
            if not self.conn:
                self.connect()
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            results = cursor.fetchall()
            cursor.close()
            logger.info("Query executed successfully")
            return results
        except Exception as e:
            logger.error("Error in querying master data:", e)
            return None

    def get_json_data(self, page=1, per_page=25):
        signals, _ = self.preferences_to_params()
        results = self.get_master_data(page, per_page)
        result_dict = []
        total_count, total_pages = self.get_dataset_size(per_page=per_page)
        for data_tuple in results:
            data_dict = {}
            for i, col_name in enumerate(signals):
                data_dict[col_name] = data_tuple[i]
            result_dict.append(data_dict)

        results = {
            "data": result_dict,
            "status": "SUCCESS",
            "page": page,
            "total_count": total_count,
            "total_pages": total_pages,
        }
        return results

    def search_data(self, search_query, params=None):
        try:
            if not self.conn:
                self.connect()
            cursor = self.conn.cursor()
            cursor.execute(search_query, params)
            column_names = [desc[0] for desc in cursor.description]
            # result = cursor.fetchall()
            result_data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

            cursor.close()
            if result_data == []:
                return {"message": "company not found in database"}
            else:
                return result_data
        except Exception as e:
            logger.error(f"Search Query error - {e}")
            raise e
