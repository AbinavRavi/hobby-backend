import base64
import json


def encode_data(data):
    data_json = json.dumps(data)
    encoded_data = base64.b64encode(data_json.encode("utf-8")).decode("utf-8")
    return encoded_data
