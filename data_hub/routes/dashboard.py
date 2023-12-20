from fastapi import APIRouter
from data_hub.utils.filter import DashboardData
from data_hub.utils.log import logger
from data_hub.utils.encode import encode_data

dashboard_router = APIRouter()


@dashboard_router.get("/show_dashboard_data/{user_id}")
async def show_data_preferences(user_id: str, page: int, per_page: int):
    id = str(user_id)
    dash = DashboardData(user_id=id)
    data = dash.fetch_dashboard_data(page=page, per_page=per_page)
    logger.info(f" the output of endpoint for showing data - {data}")
    output = encode_data(data)
    return {"data": output}


@dashboard_router.get("/search/{user_id}")
async def search(user_id: str, company_name: str):
    id = str(user_id)
    dash = DashboardData(user_id=id)
    data = dash.search_company(company_name=company_name)
    output = encode_data(data)
    return {"data": output}


@dashboard_router.get("/search_by_id/{user_id}")
async def search_by_id(user_id: str, company_id: str):
    id = str(user_id)
    dash = DashboardData(user_id=id)
    data = dash.search_company_id(company_id=company_id)
    output = encode_data(data)
    return {"data": output}
