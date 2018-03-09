
# coding: utf-8

# In[ ]:


import sys
import os
from datetime import datetime
from crawler_model_1111 import *
from util import *

def main():
    
    para_dict={'save':'F'}
    #need dire_para, rang, sect, (save) parameters
    
    print '=========='
    for para in sys.argv[1:]:
        tmp_ls=para.split("=")
        if len(tmp_ls)==2:
            print tmp_ls[0]+":"+tmp_ls[1]
            para_dict[tmp_ls[0]]=tmp_ls[1]
        else:
            raise Exception('Error in input "'+para+'". please use "name1=value1 name2=value2" format')
    
    try:
        para_dict['dire_para']
    except:
        para_dict['dire_para']=os.getcwd()
        print 'using default directory: '+para_dict['dire_para']
    try:
        para_dict['rang']
    except:
        para_dict['rang']='17-18'
        print 'using default rang: '+para_dict['rang']
    try:
        para_dict['sect']
    except:
        para_dict['sect']='99'
        print 'using default sect name: '+para_dict['sect']
    
    print '=========='
    
    #check if directory exist
    if not os.path.isdir(para_dict['dire_para']):
        raise Exception(para_dict['dire_para']+' doesn\'t exist')
    
    #crawler
    logtext=crawl_1111(para_dict['dire_para'],map(int,str.split(para_dict['rang'],'-')),para_dict['sect'])
    
    if para_dict['save']=='T':
        if not os.path.isdir(para_dict['dire_para']+'log/'):
            os.makedirs(para_dict['dire_para']+'log/')
        fo=open(para_dict['dire_para']+'log/log'+datetime.today().strftime("%y%m%d")+'.txt', 'w')
        fo.write(logtext)
        fo.close()
    
    
    
if __name__== "__main__":
    main()

