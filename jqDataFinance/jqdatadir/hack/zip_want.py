# encoding:utf-8

import zipfile
import os
from threading import Thread
import time
from itertools import product
from pathlib import Path

path = r'G:\\video\日本\[多P]某体校运动系美女和两个社会青年野战3P晚上街头露出\某体校运动系美女.zip'
my_pass_dict = r'dict\\'

def password(x = 6):
    # iter = ['1234567890abcdefghijklmnopqrstuvwxyz.',]
    iter = ['1234567890htpwuflixyz',]
    for r in iter:
        for repeat in range(1,x+1):
            for ps in product(r,repeat = repeat):
                yield ''.join(ps)


def run(path, password):
    if path[-4:]=='.zip':
        # path = dir + '\\' + file
        #print path
        zip = zipfile.ZipFile(path,"r",zipfile.zlib.DEFLATED)
        try:
            zip.extractall(path=="G:\\\\video\\日本\\[多P]某体校运动系美女和两个社会青年野战3P晚上街头露出",members=zip.namelist(),pwd=password)
            print('-----success,The password is %s '%password)
            zip.close()
            return True
        except:
            print(' ------error!,The password is %s'%password)

if __name__ == '__main__':
    start=time.clock()
    p = Path(my_pass_dict)
    dictfiles = p.glob('*/*.txt')

    for ps in password(8):
        if(run(path,ps)):
            break
    print("done (%.2f second)"%(time.clock() - start))