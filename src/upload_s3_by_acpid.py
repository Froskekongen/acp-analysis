from boto.s3.connection import S3Connection
from boto.s3.key import Key
import glob
import sys
import json
from process_json import get_analysis_data
#print(sys.argv)

files = glob.glob('/mnt/es-data/*.json')
conn=S3Connection(sys.argv[1],sys.argv[2])
bucket=conn.get_bucket('s3-acpcontent')

for fn in files:
    with open(fn) as ff:
        jsonObjs=json.load(ff)

    dumpdata=[]
    n_data=0
    key_nr=0
    nr_len=len(str(len(jsonObjs)))
    for iii,jo in enumerate(jsonObjs):
        if 'fields' in jo['_source']:
            if 'body' in jo['_source']['fields']:
                nd=get_analysis_data(jo)
                dumpdata.append(nd)
                n_data+=1
                if n_data%1000==0:


                    print('analysis data gotten')
                    k=Key(bucket)
                    kkey=nd['_index']+'/'+nd['_index']+'_'+str(n_data).zfill(nr_len)+'_'+str(key_nr)+'.json'
                    k.key=kkey
                    nd_as_string=json.dumps(dumpdata)
                    k.set_contents_from_string(nd_as_string)
                    key_nr+=1
                    dumpdata.clear()
                    print('what is love?',kkey)

    if (n_data%1000)!=0:
        k=Key(bucket)
        kkey=nd['_index']+'/'+nd['_index']+'_'+str(n_data).zfill(nr_len)+'_'+str(key_nr)+'.json'
        k.key=kkey
        nd_as_string=json.dumps(nd)
        k.set_contents_from_string(nd_as_string)
        key_nr+=1
        dumpdata.clear()
        print('what is love?')
