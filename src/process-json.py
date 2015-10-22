import ijson
import json
import glob
from pprint import pprint

import re
import matplotlib.pyplot as plt
import numpy as np

PAR_RE = re.compile(r'<p>')
TAG_RE = re.compile(r'<[^>]+>')

GET_ACPID=re.compile(r'/([0-9]+\-[0-9]+\-[0-9]+)\.')

def process_body(txt):
    re_txt=PAR_RE.sub('\n',txt)
    re_txt=TAG_RE.sub('',re_txt)
    return re_txt

def get_acpids(src):
    acpids=[]
    if '_alternates' in src:
        for link in src['_alternates']:
            acpid=GET_ACPID.findall(link)[0]
            acpids.append(acpid)
    if len(acpids)>0:
        return acpids
    else:
        return False

def get_analysis_data(dd):
    indexname=dd['_index']
    idcontent=dd['_id']
    if '_source' not in dd:
        return False
    src=dd['_source']
    acpids=get_acpids(src)
    
    if acpids:
        fns=acpids
    else:
        fns=[indexname+'-'+idcontent]






files = glob.glob('../data/*.json')
caseLengths=[]
for pp in files:
    with open(pp) as ff:

        jsonObj=json.load(ff)
        for jo in jsonObj:
            fns=[]
            try:
                acpids=[]
                for link in jo['_source']['_alternates']:
                    acpid=GET_ACPID.findall(link)[0]
                    acpids.append(acpid)
                    fns.append(acpid)

            except exception as E:
                fns.extend(jo['_index']+'-'+jo['_id'])
            try:
                ret_obj={'body':process_body(jo['_source'][''])}
            except:
                continue
            ret_obj['id']=jo['_id']
            ret_obj['acp-id']=



caseLengths=np.array(caseLengths)
caseLengths.sort()
print(len(caseLengths))
plt.hist(caseLengths[:5000])
plt.show()
