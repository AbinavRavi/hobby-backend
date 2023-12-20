from fastapi import APIRouter
from data_hub.utils.openai import Enrichment
from data_hub.utils.save_company import SaveCompanyDetails
from data_hub.utils.log import logger

ai_router = APIRouter()


@ai_router.get("/enrich_company/{user_id}")
def enrich_account_details(company_id: str, user_id: str):
    enrich = Enrichment(user_id, company_id)
    result = enrich.enrich_company()
    save = SaveCompanyDetails(user_id=user_id, company_id=company_id)
    status = save.write_data(result["response"])
    logger.info(f"write status into database - {status}")
    return result
