from data_hub.utils.database_ops import PreferencesDataOps, DashboardOps
from data_hub.utils.metadata import MetadataDbOps
from data_hub.utils.log import logger
from dotenv import load_dotenv
import json
import os


class DashboardData:
    def __init__(self, user_id):
        self.user_id = user_id

    def fetch_preferences(self):
        pref_db = PreferencesDataOps()
        try:
            document = pref_db.find_document(self.user_id, self.user_id)
            logger.info(f"preference document - {document}")
            preferences = json.loads(document["preferences"])
            return preferences
        except Exception as e:
            logger.error(f"Fetching preferences from database resulted in an error: {e}")
            return None

    def fetch_dashboard_data(self, page, per_page=25):
        dash_db = DashboardOps(self.user_id, self.fetch_preferences())
        logger.debug(f"fetching data for {self.user_id} with {self.fetch_preferences()}")
        data = dash_db.get_json_data(page=page, per_page=per_page)
        return data

    def search_company(self, company_name: str):
        load_dotenv()
        table_name = os.getenv("MASTER_DB_TABLE_NAME")
        db = DashboardOps(self.user_id, self.fetch_preferences())
        logger.info(f"searching for {company_name}")
        search_query = f"SELECT * FROM {table_name} WHERE company_name = %s"
        search_result = db.search_data(search_query, params=(str(company_name),))
        return search_result

    def search_company_id(self, company_id: str):
        load_dotenv()
        table_name = os.getenv("MASTER_DB_TABLE_NAME")
        db = DashboardOps(self.user_id, self.fetch_preferences())
        logger.info(f"searching for {company_id}")
        search_query = f"SELECT * FROM {table_name} WHERE company_id = %s"
        search_result = db.search_data(search_query, params=(str(company_id),))
        return search_result

    def get_metadata_id(self, company_id: str):
        load_dotenv()
        db = MetadataDbOps()
        all_data = db.read_metadata()
        return all_data
