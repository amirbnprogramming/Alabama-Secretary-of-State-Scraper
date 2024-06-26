from encodings.utf_8 import decode

import pandas as pd

from Utils.logger import logger


def bussiness_data_normalizer(data):
    processed_data = []
    for key, value in data.items():
        row = {
            'Id': key,
            'Link': value['Link'],
            'Entity ID Number': value['Entity ID Number'],
            'Entity Type': value['Entity Type'],
            'Principal Address': value['Principal Address'],
            'Principal Mailing Address': value['Principal Mailing Address'],
            'Status': value['Status'],
            'Place of Formation': value['Place of Formation'],
            'Registered Agent Name': value['Registered Agent Name'],
            'Registered Office Street Address': value['Registered Office Street Address'],
            'Registered Office Mailing Address': value['Registered Office Mailing Address'],
            'Nature of Business': value['Nature of Business'],
        }
        processed_data.append(row)
    return processed_data


def bussiness_csv_saver(data, path):
    pre_processed_data = bussiness_data_normalizer(data)
    df = pd.DataFrame(pre_processed_data)
    df.to_csv(path, index=False)
    logger.warning(f"Item's File saved to {path}")
