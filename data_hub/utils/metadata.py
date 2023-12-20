import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from data_hub.utils.log import logger


class MetadataDbOps:
    def __init__(self) -> None:
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

    def get_master_data_batch(self):
        try:
            if not self.conn:
                self.connect()
            cursor = self.conn.cursor()
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
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

    def calculate_metdata(self):
        metadata = []
        data = self.get_master_data_batch()
        for datum in data:
            company_id = datum["company_id"]
            hiring = HiringMetadata(datum)
            hiring_md = hiring.hiring_metadata()
            funding = FundingMetadata(datum)
            funding_md = funding.funding_metadata()
            traffic = TrafficMetadata(datum)
            traffic_md = traffic.traffic_metadata()
            metadict = {**hiring_md, **funding_md, **traffic_md}
            metadict["company_id"] = company_id
            metadata.append(metadict)
        return metadata

    def write_data(self):
        metadata = self.calculate_metdata()
        df = pd.DataFrame(metadata)
        try:
            load_dotenv()
            db_params = {
                "database": os.getenv("MASTER_DB_NAME"),
                "user": os.getenv("MASTER_DB_USER"),
                "password": os.getenv("MASTER_DB_PASSWORD"),
                "host": os.getenv("MASTER_DB_HOST"),
                "port": os.getenv("MASTER_DB_PORT"),
            }

            # Establish a connection to the PostgreSQL database
            connection = psycopg2.connect(**db_params)
            engine = create_engine(
                f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}'
            )
            # remove the comment for the below line if it throws an exception with column name
            # df.drop(columns=["glassdoor_ceo_approval_mom_pct"], inplace=True)
            # Dump the DataFrame into PostgreSQL
            rows = df.to_sql("metadata", engine, if_exists="append", index=False)
            print(rows)
            # Close the connection
            connection.close()
            return True
        except Exception as e:
            raise Exception(f"Error inserting data into PostgreSQL: {str(e)}")

    def read_metadata(self):
        pass


class MetadataGen:
    def __init__(self, company_details):
        self.company_details = company_details


class HiringMetadata(MetadataGen):
    def __init__(self, company_details):
        super().__init__(company_details)
        self.li_hiring_month = self.company_details["linkedin_headcount_mom_percent"]
        self.li_hiring_quarter = self.company_details["linkedin_headcount_qoq_percent"]
        self.li_hiring_year = self.company_details["linkedin_headcount_yoy_percent"]
        self.jobs_count_month = self.company_details["job_openings_count_mom_pct"]
        self.jobs_count_quarter = self.company_details["job_openings_count_qoq_pct"]
        self.jobs_count_year = self.company_details["job_openings_count_yoy_pct"]

    def hiring_metadata(self):
        if (
            self.li_hiring_month is None
            or self.li_hiring_quarter is None
            or self.li_hiring_year is None
        ):
            return {"hiring_growth": "Data Not Available"}
        elif self.li_hiring_month > 0 and self.li_hiring_quarter <= 0 and self.li_hiring_year <= 0:
            return {"hiring_growth": "Increased Hiring Last Month"}
        elif self.li_hiring_month <= 0 and self.li_hiring_quarter > 0 and self.li_hiring_year <= 0:
            return {"hiring_growth": "Increased Hiring Last Quarter"}
        elif self.li_hiring_month <= 0 and self.li_hiring_quarter <= 0 and self.li_hiring_year > 0:
            return {"hiring_growth": "Increased Hiring Last Year"}
        elif self.li_hiring_month > 0 and self.li_hiring_quarter > 0 and self.li_hiring_year <= 0:
            return {"hiring_growth": "Increased Hiring Last Month and Quarter"}
        elif self.li_hiring_month > 0 and self.li_hiring_quarter <= 0 and self.li_hiring_year > 0:
            return {"hiring_growth": "Increased Hiring Last Month and Year"}
        elif self.li_hiring_month <= 0 and self.li_hiring_quarter > 0 and self.li_hiring_year > 0:
            return {"hiring_growth": "Increased Hiring Last Quarter and Year"}
        elif self.li_hiring_month > 0 and self.li_hiring_quarter > 0 and self.li_hiring_year > 0:
            return {"hiring_growth": "Increased Hiring Across All Timeframes"}
        else:
            return {"hiring_growth": "No Recent Increase in Hiring"}


class FundingMetadata(MetadataGen):
    def __init__(self, company_details):
        super().__init__(company_details)
        self.funding = self.company_details["crunchbase_total_investment_usd"]
        self.days_since_funding = self.company_details["days_since_last_fundraise"]
        self.valuation = self.company_details["valuation_usd"]
        self.vc_backed = self.company_details["crunchbase_investors"]

    def funding_metadata(self):
        if self.days_since_funding is None:
            recent_funding = "Data Not Available"
        elif self.days_since_funding <= 30:
            recent_funding = "Recently Funded"
        elif self.days_since_funding <= 365:
            recent_funding = "Funded This Year"
        else:
            recent_funding = "No Recent Funding"

        if self.funding is None:
            consistent_funding = "Data Not Available"
        elif self.funding > 0:
            consistent_funding = "Currently Raising"
        else:
            consistent_funding = "Not Currently Raising"

        if self.valuation is None:
            company_stage = "Data Not Available"
        elif self.valuation >= 10000000000:
            company_stage = "Decacorn"
        elif self.valuation >= 1000000000:
            company_stage = "Unicorn"
        elif self.valuation >= 500000000:
            company_stage = "Soonicorn"
        elif self.valuation >= 50000000:
            company_stage = "Late Stage"
        elif self.valuation >= 10000000:
            company_stage = "Growth Stage"
        elif self.valuation >= 5000000:
            company_stage = "Scale Up"
        else:
            company_stage = "Startup"

        if self.vc_backed is None:
            spend_potential = "Data Not Available"
        elif self.vc_backed:
            spend_potential = "High Spend Potential"
        else:
            spend_potential = "Low Spend Potential"

        return {
            "recent_funding": recent_funding,
            "consistent_funding": consistent_funding,
            "company_stage": company_stage,
            "spend_potential": spend_potential,
        }


class TrafficMetadata(MetadataGen):
    def __init__(self, company_details):
        super().__init__(company_details)
        self.traffic_social_pct = self.company_details["traffic_source_social_pct"]
        self.traffic_search_pct = self.company_details["traffic_source_search_pct"]
        self.traffic_direct_pct = self.company_details["traffic_source_direct_pct"]
        self.traffic_paid_referral_pct = self.company_details["traffic_source_paid_referral_pct"]
        self.traffic_source_referral_pct = self.company_details["traffic_source_referral_pct"]
        self.mata_ads = self.company_details["meta_total_ads"]
        self.meta_active_ads = self.company_details["meta_active_ads"]
        self.organic_rank = self.company_details["average_organic_rank"]
        self.monthly_paid_clicks = self.company_details["monthly_paid_clicks"]
        self.monthly_organic_clicks = self.company_details["monthly_organic_clicks"]
        self.average_ad_rank = self.company_details["average_ad_rank"]
        self.total_organic_results = self.company_details["total_organic_results"]
        self.monthly_google_ads_budget = self.company_details["monthly_google_ads_budget"]
        self.monthly_organic_value = self.company_details["monthly_organic_value"]
        self.total_ads_purchased = self.company_details["total_ads_purchased"]
        self.lost_ranks = self.company_details["lost_ranks"]
        self.gained_ranks = self.company_details["gained_ranks"]
        self.newly_ranked = self.company_details["newly_ranked"]
        self.paid_competitors = self.company_details["paid_competitors"]
        self.organic_competitors = self.company_details["organic_competitors"]

    def traffic_metadata(self):
        if self.traffic_social_pct is not None and self.traffic_social_pct > 0.5:
            website_size = "High Traffic"
        else:
            website_size = "Low Traffic"

        if self.traffic_search_pct is not None:
            if self.traffic_search_pct > 0:
                traffic_growth = "Consistent Growth"
            elif self.traffic_search_pct < 0:
                traffic_growth = "Consistent Loss"
            else:
                traffic_growth = "Sudden Spike"
        else:
            traffic_growth = "Data Not Available"

        if self.traffic_social_pct is not None:
            if self.traffic_social_pct > 0.5:
                viral_status = "Possibly Viral"
            else:
                viral_status = "Not Viral"
        else:
            viral_status = "Data Not Available"

        if self.traffic_direct_pct is not None:
            if self.traffic_direct_pct > 0:
                growth_recency = "Last Month"
            elif self.traffic_paid_referral_pct is not None and self.traffic_paid_referral_pct > 0:
                growth_recency = "Last Quarter"
            else:
                growth_recency = "Last Year"
        else:
            growth_recency = "Data Not Available"

        if self.traffic_search_pct is not None and self.traffic_social_pct is not None:
            if self.traffic_search_pct > self.traffic_social_pct:
                traffic_source = "Search Heavy"
            else:
                traffic_source = "Social Heavy"
        else:
            traffic_source = "Data Not Available"

        if (
            self.monthly_paid_clicks is not None
            and self.monthly_organic_clicks is not None
            and self.total_organic_results is not None
            and self.total_ads_purchased is not None
            and self.traffic_source_referral_pct is not None
        ):
            if self.monthly_paid_clicks > self.monthly_organic_clicks:
                growth_inference = "PPC Driven"
            elif self.total_organic_results > self.total_ads_purchased:
                growth_inference = "SEO Driven"
            elif self.traffic_source_referral_pct > 0.5:
                growth_inference = "Partnership Driven"
            else:
                growth_inference = "Content Driven"
        else:
            growth_inference = "Data Not Available"

        return {
            "website_size": website_size,
            "traffic_growth": traffic_growth,
            "viral_status": viral_status,
            "growth_recency": growth_recency,
            "traffic_source": traffic_source,
            "growth_inference": growth_inference,
        }


class GrowthMetadata(MetadataGen):
    def __init__(self, company_details):
        super().__init__(company_details)

    def growth_metadata(self):
        pass


if __name__ == "__main__":
    meta = MetadataDbOps()
    data = meta.write_data()
    print(data)
