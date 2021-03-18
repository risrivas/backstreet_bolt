import io
import boto3
import pandas as pd
import zipfile
from pyarrow.feather import write_feather


def read_zip_file_from_s3(s3_url):
    assert s3_url.startswith("s3://")
    bucket_name, key_name = s3_url[5:].split("/", 1)

    print(bucket_name)
    print(key_name)

    s3_resource = boto3.resource('s3', aws_access_key_id='AKIAVTMOLD5RH2X4JCJS', aws_secret_access_key='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')
    zip_obj = s3_resource.Object(bucket_name=bucket_name, key=key_name)
    buffer = io.BytesIO(zip_obj.get()['Body'].read())

    z = zipfile.ZipFile(buffer)
    for filename in z.namelist():
        # file_info = z.getinfo(filename) 
        print(filename)

def write_feather_to_s3(s3_url, symbol):
    assert s3_url.startswith("s3://")
    bucket_name, key_name = s3_url[5:].split("/", 1)

    print(bucket_name)
    print(key_name)

    df = pd.read_feather(f'data/feathers/daily/{symbol}.feather')
    s3_resource = boto3.resource('s3', aws_access_key_id='AKIAVTMOLD5RH2X4JCJS', aws_secret_access_key='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')
    with io.BytesIO() as f:
        write_feather(df, f)
        s3_resource.Object(bucket_name=bucket_name, key=key_name).put(Body=f.getvalue())

def read_feather_from_s3(s3_url):
    # s3://bbfirstdata/individual/Data/
    assert s3_url.startswith("s3://")
    bucket_name, key_name = s3_url[5:].split("/", 1)

    print(bucket_name)
    print(key_name)

    s3_resource = boto3.resource('s3', aws_access_key_id='AKIAVTMOLD5RH2X4JCJS', aws_secret_access_key='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')
    fthr_obj = s3_resource.Object(bucket_name=bucket_name, key=key_name)
    buffer = io.BytesIO(fthr_obj.get()['Body'].read())

    return pd.read_feather(buffer)

if __name__ == '__main__':
    # s3_url = 's3://team06-shared-space/MarketData/ChinaAShares/daily/1_1000.zip'
    # read_zip_file_from_s3(s3_url)
    # symbol = '600276.SS'
    symbol = 'F'
    # s3_url = f's3://team06-shared-space/MarketData/ChinaAShares/daily/{symbol}.feather'
    s3_url = f's3://bbfirstdata/individual/Data/{symbol}.feather'
    write_feather_to_s3(s3_url, symbol)
    df = read_feather_from_s3(s3_url)
    print(df.tail())



