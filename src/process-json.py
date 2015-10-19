import ijson
import json
import glob
from pprint import pprint

import re
import matplotlib.pyplot as plt
import numpy as np

PAR_RE = re.compile(r'<.?p>')
TAG_RE = re.compile(r'<[^>]+>')



files = glob.glob('../data/*.json')
caseLengths=[]
for pp in files:
    with open(pp) as ff:
        jsonObj=json.load(ff)
        for jo in jsonObj:
            jo=jo['_source']
            if 'body' in jo['fields']:
                caseLengths.append(len(jo['fields']['body']))
                if len(jo['fields']['body'])>200:
                    jo['fields']['body']=PAR_RE.sub('\n',jo['fields']['body'])
                    jo['fields']['body']=TAG_RE.sub('',jo['fields']['body'])
                    jo['fields']['body']=jo['fields']['body'].strip()

                    # pprint(jo)
                    # input()


caseLengths=np.array(caseLengths)
caseLengths.sort()
print(len(caseLengths))
plt.hist(caseLengths[:5000])
plt.show()
