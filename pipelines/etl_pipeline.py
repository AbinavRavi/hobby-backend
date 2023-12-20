import requests
import pandas as pd
import json
from dotenv import load_dotenv
import os
from prefect import flow, task
import psycopg2
from sqlalchemy import create_engine


@task
def crustdata_api_call(data, offset):
    load_dotenv()
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://crustdata.com",
        "Authorization": f"Token {os.getenv('CRUSTDATA_API_KEY')}",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }
    print(header)
    offset = offset  # Initial offset
    data["offset"] = offset
    try:
        response = requests.request(
            "POST", url="https://crustdata.com/screener/screen/", headers=header, json=data
        )
        return response.json()
    except Exception as e:
        print(f"API call failed to crustdata due to {e}")
        return e


def transform_to_dataframe(responses) -> pd.DataFrame:
    try:
        combined_df = None

        for response in responses:
            field_names = [
                response["fields"][i]["api_name"] for i in range(len(response["fields"]))
            ]
            values = response["rows"]

            df = pd.DataFrame(values, columns=field_names)

            if combined_df is None:
                combined_df = df
            else:
                combined_df = pd.concat([combined_df, df], ignore_index=True)
        return combined_df
    except Exception as e:
        raise Exception(f"Error transforming data to dataframe: {str(e)}")


# Define the function to perform the multiple insert into PostgreSQL
@task
def insert_into_postgres(df):
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
        rows = df.to_sql("table_name", engine, if_exists="append", index=False)
        print(rows)
        # Close the connection
        connection.close()
        return True
    except Exception as e:
        raise Exception(f"Error inserting data into PostgreSQL: {str(e)}")


@flow
def run_workflow():
    crustdata_filter = "./pipelines/crustdata_filter.json"
    with open(crustdata_filter) as f:
        data = json.load(f)
    offset, end_offset = 0, 2000
    api_responses = []
    while offset <= end_offset:
        data[offset] = offset
        response = crustdata_api_call(data, offset=offset)
        offset += 1000
        api_responses.append(response)
    # print(len(api_responses))
    # with open("api_response.json", "w") as json_file:
    #     json.dump(api_responses, json_file)
    df = transform_to_dataframe(api_responses)
    print(df.shape)
    status = insert_into_postgres(df)
    print(status)


if __name__ == "__main__":
    run_workflow()
