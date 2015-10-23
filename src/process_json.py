import ijson
import json
import glob
from pprint import pprint

import re
import matplotlib.pyplot as plt
import numpy as np

import html


PAR_RE = re.compile(r'</p>')
TAG_RE = re.compile(r'<[^>]+>')
REPEATING_NEWLINES_RE=re.compile(r'(\s)\1{2,}',re.UNICODE)
EXPLICIT_NEWLINE_RE=re.compile(r'\n')

GET_ACPID=re.compile(r'/([0-9]+\-[0-9]+\-[0-9]+)\.')

def process_body(txt):
    re_txt=EXPLICIT_NEWLINE_RE.sub(' ',txt)
    re_txt=PAR_RE.sub('\n\n',re_txt)
    re_txt=TAG_RE.sub('',re_txt)
    re_txt=re_txt.strip()
    re_txt=REPEATING_NEWLINES_RE.sub(r'\1\1',re_txt)
    return html.unescape(re_txt)

def get_body(src):
    #pprint(src['fields'])
    try:
        txt_raw=src['fields']['body']
        txt=process_body( txt_raw )
    except Exception as e:
        print('fields, body not found',e)
        txt=None
        txt_raw=None
    return txt,txt_raw

def get_acpids(src):
    acpids=[]
    if 'alternates' in src:
        for link in src['alternates']:
            acpid=GET_ACPID.findall(link)[0]
            acpids.append(acpid)
    if len(acpids)>0:
        return acpids
    else:
        return False

def get_tags(src):
    tags=[]
    if 'tags' in src:
        for tag in src['tags']:
            tags.append(tag['name'])
    return tags


def get_analysis_data(dd):
    src_fields=['alternates','authors','authorsUntouched','creationDate','creator']
    fields_fields=['byline','leadtext','title','lastModifiedDate','publishedDate','lastEditedUser']
    indexname=dd['_index']
    idcontent=dd['_id']
    if '_source' not in dd:
        return False
    src=dd['_source']
    acpids=get_acpids(src)
    tags=get_tags(src)
    body,body_raw=get_body(src)



    if acpids:
        fns=acpids
    else:
        fns=[indexname+'-'+idcontent]

    dd['acpids']=acpids
    dd['filenames']=fns
    dd['new_id']=indexname+'-'+str(idcontent)
    dd['text_processed']=body
    dd['tags_processed']=tags

    return dd







#
# files = glob.glob('../data/*.json')
# caseLengths=[]
#
# objs=[]
#
# for pp in files:
#     processed=pp+'_processed'
#     with open(pp) as ff, open(processed,'w') as ff2:
#
#         jsonObj=json.load(ff)
#         for jo in jsonObj:
#             if 'fields' in jo['_source']:
#                 if 'body' in jo['_source']['fields']:
#                     #pprint(jo)
#                     nd=get_analysis_data(jo)
#                     # print(nd['text'])
#                     # try:
#                     #     print(nd['title'])
#                     # except:
#                     #     pass
#                     #print(nd['tags'])
#                     #print(nd['acpids'])
#                     objs.append(nd)
#         json.dump(objs,ff2)
