import json
import pandas as pd

with open("/Users/abinavr/Desktop/namora/api.json") as f:
    data = json.load(f)

number_of_fields = data["fields"][0]
number_of_items_in_row = len(data["rows"][0])

field_names =  [data["fields"][i]["api_name"] for i in range(len(data["fields"]))]
# field_types = [data["fields"][i]["type"] for i in range(len(data["fields"]))]
values = data["rows"]

df = pd.DataFrame(values, columns=field_names)
# df.to_csv("/Users/abinavr/Desktop/namora/api.csv")


def get_column_data_types(df):
    column_data_types = {}
    
    for column_name, dtype in df.dtypes.items():
        column_data_types[column_name] = str(dtype)
    
    return column_data_types

schema = json.dumps(get_column_data_types(df))

with open("/Users/abinavr/Desktop/namora/db_schema.json", "w") as f:
    json.dump(get_column_data_types(df), f, indent=4)