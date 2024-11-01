CREATE TABLE IF NOT EXISTS companies  (
  company_id SERIAL PRIMARY KEY,
  company_name TEXT NOT NULL,
  valuation_usd FLOAT NOT NULL,
  crunchbase_total_investment_usd FLOAT,
  markets TEXT,
  days_since_last_fundraise INT,
  linkedin_headcount INT,
  linkedin_headcount_mom_percent FLOAT,
  linkedin_headcount_qoq_percent FLOAT,
  linkedin_headcount_yoy_percent FLOAT,
  linkedin_headcount_mom_absolute INT,
  linkedin_headcount_qoq_absolute INT,
  linkedin_headcount_yoy_absolute INT,
  glassdoor_overall_rating FLOAT,
  glassdoor_ceo_approval_pct FLOAT,
  glassdoor_business_outlook_pct FLOAT,
  glassdoor_review_count INT,
  g2_review_count INT,
  g2_average_rating FLOAT,
  hq_country TEXT,
  largest_headcount_country TEXT,
  last_funding_round_type TEXT,
  company_website TEXT,
  company_website_domain TEXT,
  valuation_date DATE,
  linkedin_categories TEXT,
  linkedin_industries TEXT,
  crunchbase_investors TEXT,
  crunchbase_categories TEXT,
  linkedin_profile_url TEXT,
  acquisition_status TEXT,
  company_year_founded INT,
  technology_domains TEXT,
  founder_names_and_profile_urls TEXT,
  founders_location TEXT,
  founders_education_institute TEXT,
  founders_degree_name TEXT,
  founders_previous_company TEXT,
  founders_previous_title TEXT,
  monthly_visitors FLOAT,
  monthly_visitor_mom_pct FLOAT,
  traffic_source_social_pct FLOAT,
  traffic_source_search_pct FLOAT,
  traffic_source_direct_pct FLOAT,
  traffic_source_paid_referral_pct FLOAT,
  traffic_source_referral_pct FLOAT,
  meta_total_ads FLOAT,
  meta_active_ads FLOAT,
  meta_ad_platforms TEXT,
  meta_ad_url TEXT,
  meta_ad_id TEXT,
  average_organic_rank FLOAT,
  monthly_paid_clicks FLOAT,
  monthly_organic_clicks FLOAT,
  average_ad_rank FLOAT,
  total_organic_results FLOAT,
  monthly_google_ads_budget FLOAT,
  monthly_organic_value FLOAT,
  total_ads_purchased FLOAT,
  lost_ranks INT,
  gained_ranks INT,
  newly_ranked INT,
  paid_competitors TEXT,
  organic_competitors TEXT,
  linkedin_id TEXT,
  linkedin_followers INT,
  linkedin_headcount_engineering INT,
  linkedin_headcount_sales INT,
  linkedin_headcount_operations INT,
  linkedin_headcount_human_resource INT,
  linkedin_headcount_india INT,
  linkedin_headcount_usa INT,
  linkedin_headcount_engineering_percent FLOAT,
  linkedin_headcount_sales_percent FLOAT,
  linkedin_headcount_operations_percent FLOAT,
  linkedin_headcount_human_resource_percent FLOAT,
  linkedin_headcount_india_percent FLOAT,
  linkedin_headcount_usa_percent FLOAT,
  linkedin_followers_mom_percent FLOAT,
  linkedin_followers_qoq_percent FLOAT,
  linkedin_followers_yoy_percent FLOAT,
  glassdoor_culture_rating FLOAT,
  glassdoor_diversity_rating FLOAT,
  glassdoor_work_life_balance_rating FLOAT,
  glassdoor_senior_management_rating FLOAT,
  glassdoor_compensation_rating FLOAT,
  glassdoor_career_opportunities_rating FLOAT,
  glassdoor_recommend_to_friend_pct TEXT,
  glassdoor_ceo_approval_mom_pct FLOAT,
  glassdoor_ceo_approval_qoq_pct FLOAT,
  glassdoor_review_count_mom_pct FLOAT,
  glassdoor_review_count_qoq_pct FLOAT,
  glassdoor_review_count_yoy_pct FLOAT,
  g2_review_count_mom_pct FLOAT,
  g2_review_count_qoq_pct FLOAT,
  g2_review_count_yoy_pct FLOAT,
  instagram_followers FLOAT,
  instagram_posts TEXT,
  instagram_followers_mom_pct FLOAT,
  instagram_followers_qoq_pct FLOAT,
  instagram_followers_yoy_pct FLOAT,
  recent_job_openings_title TEXT,
  recent_job_openings_title_count FLOAT,
  job_openings_count FLOAT,
  job_openings_count_mom_pct FLOAT,
  job_openings_count_qoq_pct FLOAT,
  job_openings_count_yoy_pct FLOAT,
  job_openings_accounting_qoq_pct FLOAT,
  job_openings_accounting_six_months_growth_pct FLOAT,
  job_openings_art_and_design_qoq_pct FLOAT,
  job_openings_art_and_design_six_months_growth_pct FLOAT,
  job_openings_business_development_qoq_pct FLOAT,
  job_openings_business_development_six_months_growth_pct FLOAT,
  job_openings_engineering_qoq_pct FLOAT,
  job_openings_engineering_six_months_growth_pct FLOAT,
  job_openings_finance_qoq_pct FLOAT,
  job_openings_finance_six_months_growth_pct FLOAT,
  job_openings_human_resource_qoq_pct FLOAT,
  job_openings_human_resource_six_months_growth_pct FLOAT,
  job_openings_information_technology_qoq_pct FLOAT,
  job_openings_information_technology_six_months_growth_pct FLOAT,
  job_openings_marketing_qoq_pct FLOAT,
  job_openings_marketing_six_months_growth_pct FLOAT,
  job_openings_media_and_communication_qoq_pct FLOAT,
  job_openings_media_and_communication_six_months_growth_pct FLOAT,
  job_openings_operations_qoq_pct FLOAT,
  job_openings_operations_six_months_growth_pct FLOAT,
  job_openings_research_qoq_pct FLOAT,
  job_openings_research_six_months_growth_pct FLOAT,
  job_openings_sales_qoq_pct FLOAT,
  job_openings_sales_six_months_growth_pct FLOAT,
  job_openings_product_management_qoq_pct FLOAT,
  job_openings_product_management_six_months_growth_pct FLOAT,
  job_openings_overall_qoq_pct FLOAT,
  job_openings_overall_six_months_growth_pct FLOAT,
  total_rows INT
);
