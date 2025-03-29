import pandas as pd
import os
import boto3

file_path = '/home/advait/Documents/SCMS_Delivery_History_Dataset.csv'

df = pd.read_csv(file_path,header=None)

api_key = os.getenv('Access_key')
api_secret = os.getenv('Secret_access_key')
bucket_name = 'supply-chain-raw-dataaaa'


def upload_file():
    s3 = boto3.client('s3')
    df = pd.read_csv(file_path, dtype='unicode')
    s3.upload_file(file_path, 'supply-chain-raw-dataaaa', 'SCMS_Delivery_History_Dataset.csv')

upload_file()


