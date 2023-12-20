from dotenv import load_dotenv
import os
from data_hub.utils.log import logger
from data_hub.utils.filter import DashboardData
from data_hub.utils.database_ops import MongoDataOps


class SaveCompanyDetails(MongoDataOps):
    def __init__(self, user_id, company_id) -> None:
        load_dotenv()
        self.db_name = os.getenv("SAVED_COMPANY_DB_NAME")
        self.uri = os.getenv("SAVED_COMPANY_DB")
        self.company_id = company_id
        self.user_id = user_id
        super().__init__(self.uri, self.db_name, collection_name=self.user_id)

    def get_company_details(self):
        db = DashboardData(self.user_id)
        company_details = db.search_company_id(self.company_id)
        return company_details[0]

    def get_ai_metadata(self):
        db = DashboardData(self.user_id)
        metadata = db.get_metadata_id(self.company_id)
        return metadata

    def write_data(self, enrich_summary):
        saved_company_document = {**self.get_company_details()}
        saved_company_document["summary"] = enrich_summary
        logger.info(f"document to save - {saved_company_document}")
        connection_status = self.connect()
        logger.info(f"connection to  database - {connection_status}")
        check_table = self.check_and_create_db(db_name=self.db_name)
        logger.info(f"check if db exists -{check_table}")
        if connection_status:
            collection_status = self.collection_exists_or_create(self.user_id)
            logger.info(f"check if collection exists -{collection_status}")
            if collection_status:
                insert_status = self.insert_data(saved_company_document)
                logger.info(f"Status of insert into the preference table -{insert_status}")
                if insert_status:
                    return True
                else:
                    return False
            else:
                return {"status": "COLLECTION ERROR"}
        else:
            return {"status": "CONNECTION ERROR"}
