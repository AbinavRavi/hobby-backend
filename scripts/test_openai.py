import os
import openai
from dotenv import load_dotenv

prompt = """
You are a research analyst who is provided with some company data to perform analysis,
Given the below json data for a particular company

{
    "company_name": "Cura Technologies",
    "valuation_usd": null,
    "crunchbase_total_investment_usd": 5038000,
    "markets": "NSE,BSE",
    "days_since_last_fundraise": 470.0,
    "linkedin_headcount": 16,
    "linkedin_headcount_mom_percent": 0.0,
    "linkedin_headcount_qoq_percent": -27.15,
    "linkedin_headcount_yoy_percent": -40.59,
    "linkedin_headcount_mom_absolute": 0.0,
    "linkedin_headcount_qoq_absolute": -6.0,
    "linkedin_headcount_yoy_absolute": -11.0,
    "glassdoor_overall_rating": null,
    "glassdoor_ceo_approval_pct": null,
    "glassdoor_business_outlook_pct": null,
    "glassdoor_review_count": null,
    "g2_review_count": null,
    "g2_average_rating": null,
    "company_id": 1088,
    "hq_country": "USA",
    "largest_headcount_country": "IND",
    "last_funding_round_type": null,
    "company_website": "http://www.curatechnologies.co.in",
    "company_website_domain": "cura.tech",
    "valuation_date": null,
    "linkedin_categories": null,
    "linkedin_industries": "Computer Software,Software Development",
    "crunchbase_investors": null,
    "crunchbase_categories": "Augmented Reality,Electronics,Hardware,Optical Communication,Software,Wearables",
    "linkedin_profile_url": "https://www.linkedin.com/company/cura-technologies-inc.",
    "acquisition_status": null,
    "company_year_founded": null,
    "technology_domains": null,
    "founder_names_and_profile_urls": null,
    "founders_location": null,
    "founders_education_institute": null,
    "founders_degree_name": null,
    "founders_previous_company": null,
    "founders_previous_title": null,
    "monthly_visitors": null,
    "monthly_visitor_mom_pct": null,
    "traffic_source_social_pct": null,
    "traffic_source_search_pct": null,
    "traffic_source_direct_pct": null,
    "traffic_source_paid_referral_pct": null,
    "traffic_source_referral_pct": null,
    "meta_total_ads": null,
    "meta_active_ads": null,
    "meta_ad_platforms": null,
    "meta_ad_url": null,
    "meta_ad_id": null,
    "average_organic_rank": null,
    "monthly_paid_clicks": null,
    "monthly_organic_clicks": null,
    "average_ad_rank": null,
    "total_organic_results": null,
    "monthly_google_ads_budget": null,
    "monthly_organic_value": null,
    "total_ads_purchased": null,
    "lost_ranks": null,
    "gained_ranks": null,
    "newly_ranked": null,
    "paid_competitors": null,
    "organic_competitors": null,
    "linkedin_id": "17880611",
    "linkedin_followers": 893,
    "linkedin_headcount_engineering": 12.0,
    "linkedin_headcount_sales": null,
    "linkedin_headcount_operations": 1.0,
    "linkedin_headcount_human_resource": null,
    "linkedin_headcount_india": 24.0,
    "linkedin_headcount_usa": 1.0,
    "linkedin_headcount_engineering_percent": 74.53,
    "linkedin_headcount_sales_percent": null,
    "linkedin_headcount_operations_percent": 6.21,
    "linkedin_headcount_human_resource_percent": null,
    "linkedin_headcount_india_percent": 149.07,
    "linkedin_headcount_usa_percent": null,
    "linkedin_followers_mom_percent": 0.11,
    "linkedin_followers_qoq_percent": 1.36,
    "linkedin_followers_yoy_percent": 9.44,
    "glassdoor_culture_rating": null,
    "glassdoor_diversity_rating": null,
    "glassdoor_work_life_balance_rating": null,
    "glassdoor_senior_management_rating": null,
    "glassdoor_compensation_rating": null,
    "glassdoor_career_opportunities_rating": null,
    "glassdoor_recommend_to_friend_pct": null,
    "glassdoor_ceo_approval_qoq_pct": null,
    "glassdoor_review_count_mom_pct": null,
    "glassdoor_review_count_qoq_pct": null,
    "glassdoor_review_count_yoy_pct": null,
    "g2_review_count_mom_pct": null,
    "g2_review_count_qoq_pct": null,
    "g2_review_count_yoy_pct": null,
    "instagram_followers": null,
    "instagram_posts": null,
    "instagram_followers_mom_pct": null,
    "instagram_followers_qoq_pct": null,
    "instagram_followers_yoy_pct": null,
    "recent_job_openings_title": null,
    "recent_job_openings_title_count": null,
    "job_openings_count": null,
    "job_openings_count_mom_pct": null,
    "job_openings_count_qoq_pct": null,
    "job_openings_count_yoy_pct": null,
    "job_openings_accounting_qoq_pct": null,
    "job_openings_accounting_six_months_growth_pct": null,
    "job_openings_art_and_design_qoq_pct": null,
    "job_openings_art_and_design_six_months_growth_pct": null,
    "job_openings_business_development_qoq_pct": null,
    "job_openings_business_development_six_months_growth_pct": null,
    "job_openings_engineering_qoq_pct": 0.0,
    "job_openings_engineering_six_months_growth_pct": -50.0,
    "job_openings_finance_qoq_pct": null,
    "job_openings_finance_six_months_growth_pct": null,
    "job_openings_human_resource_qoq_pct": null,
    "job_openings_human_resource_six_months_growth_pct": null,
    "job_openings_information_technology_qoq_pct": null,
    "job_openings_information_technology_six_months_growth_pct": null,
    "job_openings_marketing_qoq_pct": null,
    "job_openings_marketing_six_months_growth_pct": null,
    "job_openings_media_and_communication_qoq_pct": null,
    "job_openings_media_and_communication_six_months_growth_pct": null,
    "job_openings_operations_qoq_pct": null,
    "job_openings_operations_six_months_growth_pct": null,
    "job_openings_research_qoq_pct": null,
    "job_openings_research_six_months_growth_pct": null,
    "job_openings_sales_qoq_pct": null,
    "job_openings_sales_six_months_growth_pct": null,
    "job_openings_product_management_qoq_pct": null,
    "job_openings_product_management_six_months_growth_pct": null,
    "job_openings_overall_qoq_pct": 0.0,
    "job_openings_overall_six_months_growth_pct": 0.0,
    "total_rows": 6902
}

Tasks
I want you to make some inferences and answer the following questions
- Is this company growing the possible answers are growing, stagnant, shrinking
- how fast is this company growing? the possible answers are rapidly expanding, sudden growth, sudden layoff
- how recent is the growth? the possible answers are recent, steady growth, recent cuts

Output has to be a json of the above three questions 
{
growth: answer to question 1
velocity: answer to question 2
timeline : answer to question 3
}

Give me a list of features that were used for answering the question and how you answered in no less than 300 words
"""

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

if __name__ == "__main__":
    res = get_completion(prompt)
    print(res)