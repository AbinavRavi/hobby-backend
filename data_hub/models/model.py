from pydantic import BaseModel
from typing import List, Union, Any


class Preferences(BaseModel):
    geographies: List[str]
    industries: List[str]
    company_size: List[str]
    departments: List[str]
    department_size: List[str]
    signals: List[str]


class UserPreferences(BaseModel):
    name: str
    role: str
    company: str
    company_value_proposition: str
    preferences: Preferences


class CrustdataCompany(BaseModel):
    company_name: str
    valuation_usd: Union[int, str, None]
    crunchbase_total_investment_usd: Union[int, None]
    markets: str
    days_since_last_fundraise: float
    linkedin_headcount: int
    linkedin_headcount_mom_percent: float
    linkedin_headcount_qoq_percent: float
    linkedin_headcount_yoy_percent: float
    linkedin_headcount_mom_absolute: float
    linkedin_headcount_qoq_absolute: float
    linkedin_headcount_yoy_absolute: float
    glassdoor_overall_rating: float
    glassdoor_ceo_approval_pct: float
    glassdoor_business_outlook_pct: float
    glassdoor_review_count: float
    g2_review_count: Union[int, None]
    g2_average_rating: Union[float, None]
    company_id: int
    hq_country: str
    largest_headcount_country: str
    last_funding_round_type: str
    company_website: str
    company_website_domain: str
    valuation_date: Union[str, None]
    linkedin_categories: str
    linkedin_industries: str
    crunchbase_investors: Union[str, None]
    crunchbase_categories: str
    linkedin_profile_url: str
    acquisition_status: Union[str, None]
    company_year_founded: str
    technology_domains: str
    founder_names_and_profile_urls: str
    founders_location: str
    founders_education_institute: str
    founders_previous_company: str
    founders_previous_title: str
    monthly_visitors: float
    monthly_visitor_mom_pct: float
    traffic_source_social_pct: Union[float, None]
    traffic_source_search_pct: Union[float, None]
    traffic_source_direct_pct: Union[float, None]
    traffic_source_paid_referral_pct: Union[float, None]
    traffic_source_referral_pct: Union[float, None]
    meta_total_ads: Union[float, None]
    meta_active_ads: Union[float, None]
    meta_ad_platforms: Union[Any, None]
    meta_ad_url: Union[str, None]
    meta_ad_id: Union[Any, None]
    average_organic_rank: Union[int, None]
    monthly_paid_clicks: Union[int, None]
    monthly_organic_clicks: Union[int, None]
    average_ad_rank: Union[int, None]
    total_organic_results: Union[Any, None]
    monthly_google_ads_budget: Union[Any, None]
    monthly_organic_value: Union[Any, None]
    total_ads_purchased: Union[Any, None]
    lost_ranks: Union[Any, None]
    gained_ranks: Union[Any, None]
    newly_ranked: Union[Any, None]
    paid_competitors: Union[Any, None]
    organic_competitors: Union[Any, None]
    linkedin_id: Union[int, None]
    linkedin_followers: Union[float, None]
    linkedin_headcount_engineering: Union[float, None]
    linkedin_headcount_sales: Union[float, None]
    linkedin_headcount_operations: Union[float, None]
    linkedin_headcount_human_resource: Union[float, None]
    linkedin_headcount_india: Union[Any, None]
    linkedin_headcount_usa: Union[float, None]
    linkedin_headcount_engineering_percent: Union[float, None]
    linkedin_headcount_sales_percent: Union[float, None]
    linkedin_headcount_operations_percent: Union[float, None]
    linkedin_headcount_human_resource_percent: Union[float, None]
    linkedin_headcount_india_percent: Union[float, None]
    linkedin_headcount_usa_percent: Union[float, None]
    linkedin_followers_mom_percent: Union[float, None]
    linkedin_followers_qoq_percent: Union[float, None]
    linkedin_followers_yoy_percent: Union[float, None]
    glassdoor_culture_rating: Union[float, None]
    glassdoor_diversity_rating: Union[float, None]
    glassdoor_work_life_balance_rating: Union[float, None]
    glassdoor_senior_management_rating: Union[float, None]
    glassdoor_compensation_rating: Union[float, None]
    glassdoor_career_opportunities_rating: Union[float, None]
    glassdoor_recommend_to_friend_pct: Union[float, None]
    glassdoor_ceo_approval_mom_pct: Union[float, None]
    glassdoor_ceo_approval_qoq_pct: Union[float, None]
    glassdoor_review_count_mom_pct: Union[float, None]
    glassdoor_review_count_qoq_pct: Union[float, None]
    glassdoor_review_count_yoy_pct: Union[float, None]
    g2_review_count_mom_pct: Union[float, None]
    g2_review_count_qoq_pct: Union[float, None]
    g2_review_count_yoy_pct: Union[float, None]
    instagram_followers: Union[Any, None]
    instagram_posts: Union[Any, None]
    instagram_followers_mom_pct: Union[float, None]
    instagram_followers_qoq_pct: Union[float, None]
    instagram_followers_yoy_pct: Union[float, None]
    recent_job_openings_title: Union[Any, None]
    recent_job_openings_title_count: Union[Any, None]
    job_openings_count: Union[float, None]
    job_openings_count_mom_pct: Union[float, None]
    job_openings_count_qoq_pct: Union[float, None]
    job_openings_count_yoy_pct: Union[float, None]
    job_openings_accounting_qoq_pct: Union[float, None]
    job_openings_accounting_six_months_growth_pct: Union[float, None]
    job_openings_art_and_design_qoq_pct: Union[float, None]
    job_openings_art_and_design_six_months_growth_pct: Union[float, None]
    job_openings_business_development_qoq_pct: Union[float, None]
    job_openings_business_development_six_months_growth_pct: Union[float, None]
    job_openings_engineering_qoq_pct: Union[float, None]
    job_openings_engineering_six_months_growth_pct: Union[float, None]
    job_openings_finance_qoq_pct: Union[float, None]
    job_openings_finance_six_months_growth_pct: Union[float, None]
    job_openings_human_resource_qoq_pct: Union[float, None]
    job_openings_human_resource_six_months_growth_pct: Union[float, None]
    job_openings_information_technology_qoq_pct: Union[float, None]
    job_openings_information_technology_six_months_growth_pct: Union[float, None]
    job_openings_marketing_qoq_pct: Union[float, None]
    job_openings_marketing_six_months_growth_pct: Union[float, None]
    job_openings_media_and_communication_qoq_pct: Union[float, None]
    job_openings_media_and_communication_six_months_growth_pct: Union[float, None]
    job_openings_operations_qoq_pct: Union[float, None]
    job_openings_operations_six_months_growth_pct: Union[float, None]
    job_openings_research_qoq_pct: Union[float, None]
    job_openings_research_six_months_growth_pct: Union[float, None]
    job_openings_sales_qoq_pct: Union[float, None]
    job_openings_sales_six_months_growth_pct: Union[float, None]
    job_openings_product_management_qoq_pct: Union[float, None]
    job_openings_product_management_six_months_growth_pct: Union[float, None]
    job_openings_overall_qoq_pct: Union[float, None]
    job_openings_overall_six_months_growth_pct: Union[float, None]
    total_rows: int
