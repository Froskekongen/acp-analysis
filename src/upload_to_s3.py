from boto.s3.connection import S3Connection
import glob
import sys
#print(sys.argv)

files = glob.glob('../data/*.json')
conn=S3Connection(sys.argv[1],sys.argv[2])
bucket=conn.get_bucket('s3-acpcontent')

for pp in files:
    fn=pp.split('/')[-1]
    k=bucket.new_key(fn)
    k.set_contents_from_filename(pp)
