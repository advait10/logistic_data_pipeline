import pandas as pd
import boto3
from io import StringIO
from _datetime import datetime

loc = '/home/advait/PycharmProjects/logistic_data_pipeline/SCMS_Delivery_History_Dataset.csv'
# fetching buckets from AWS S3
def list_bucket():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    print(response)
    obj = s3.get_object(Bucket='supply-chain-raw-dataaaa', Key='SCMS_Delivery_History_Dataset.csv')
    body = obj['Body'].read().decode()
    return body


# Rename columns for better readability
def rename_col(body, *args, **kwargs):
    df = pd.read_csv(StringIO(body))
    df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '_', regex=True)
    df.dropna(inplace=True)
    return df


def extract_col(df):
    df.loc[:, 'Scheduled_Delivery_Date'] = pd.to_datetime(df["Scheduled_Delivery_Date"], dayfirst=True, errors="coerce")
    df.loc[:, 'Delivered_to_Client_Date'] = pd.to_datetime(df["Delivered_to_Client_Date"], dayfirst=True, errors="coerce")
    df.loc[:, 'Delivery_Recorded_Date'] = pd.to_datetime(df["Delivery_Recorded_Date"], dayfirst=True, errors="coerce")

    new_df = df[['ID', 'Project_Code', 'Country',
                 'Managed_By', 'Fulfill_Via', 'Vendor_INCO_Term', 'Shipment_Mode',
                 'Scheduled_Delivery_Date', 'Delivered_to_Client_Date',
                 'Delivery_Recorded_Date', 'Vendor', 'Brand', 'Dosage',
                 'Dosage_Form', 'Unit_of_Measure_Per_Pack_', 'Line_Item_Quantity',
                 'Line_Item_Value', 'Pack_Price', 'Unit_Price', 'Manufacturing_Site',
                 'Weight_Kilograms_', 'Freight_Cost_USD_', 'Line_Item_Insurance_USD_']]

    new_df = new_df.rename(columns=lambda x: x.rstrip("_"))
    return new_df


def upload_csv_to_s3(new_df):
    s3 = boto3.client('s3')
    convert_csv = new_df.to_csv('SCMS_Delivery_History_Dataset.csv',index=False)
    s3.upload_file(loc, 'supply-chain-processed-dataaaa', 'SCMS_Delivery_History_Dataset.csv')
    return "Upload data successfully to target bucket"

a = list_bucket()
b = rename_col(a)
c = extract_col(b)
print(upload_csv_to_s3(c))

