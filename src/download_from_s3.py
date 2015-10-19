from boto.s3.connection import S3Connection
import glob
import sys
from smart_open import s3_iter_bucket
#print(sys.argv)

conn=S3Connection(sys.argv[1],sys.argv[2])
bucket=conn.get_bucket('s3-acpcontent')

#keys = bucket.list()


for key, content in s3_iter_bucket(bucket, accept_key=lambda key: key.endswith('.json')):
    print (key, len(content))
