from fastapi import APIRouter, status
from data_hub.utils.database_ops import PreferencesDataOps
from data_hub.utils.log import logger
import json
from data_hub.models.model import UserPreferences

onboarding_router = APIRouter()


@onboarding_router.get("/check_user/{user_id}", status_code=status.HTTP_200_OK)
async def check_user(user_id: str):
    logger.info(f"Logged in user - {user_id}")
    db = PreferencesDataOps()
    user_exists = db.check_user(user_id)
    logger.info(f"User exists - {user_exists}")
    if user_exists:
        return {"user_exists": True}
    else:
        data = {}
        data["user_exists"] = False
        with open("data_hub/data/filters.json") as f:
            filter = json.load(f)
        data["preferences"] = filter
        return data


@onboarding_router.post("/get_preferences/{user_id}", status_code=status.HTTP_201_CREATED)
async def get_preferences(user_preferences: UserPreferences, user_id: str):
    logger.info(f"logged in user - {user_id}")
    document = user_preferences.model_dump_json()
    logger.info(f"user preferences for {user_id} - {document}")
    db = PreferencesDataOps()
    connection_status = db.connect()
    logger.info(f"connection to preference database - {connection_status}")
    check_table = db.check_and_create_db(db_name="preferences")
    logger.info(f"check if db exists -{check_table}")
    if connection_status:
        collection_status = db.collection_exists_or_create(user_id)
        logger.info(f"check if collection exists -{collection_status}")
        if collection_status:
            insert_status, inserted_id = db.insert_document(user_id, document, user_id)
            logger.info(
                f"Status of insert into the preference table -{insert_status}, id - {inserted_id}"
            )
            if insert_status:
                return {"status": "SUCCESS", "user_exists": True}
            else:
                return {"status": "FAILED"}
        else:
            return {"status": "COLLECTION ERROR"}
    else:
        return {"status": "CONNECTION ERROR"}


@onboarding_router.put("/update_preferences/{user_id}")
async def update_preferences(user_id: str, preferences: UserPreferences):
    db = PreferencesDataOps()
    user_exists = db.check_user(user_id)
    preference_exists = db.check_preferences(user_id)
    if user_exists and preference_exists:
        document = preferences.model_dump_json()
        update_status = db.update_document(user_id, document)
        if update_status:
            return {"status": "SUCCESS"}
        else:
            return {"status": "UPDATE FAILED"}
