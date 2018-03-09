
# coding: utf-8

# In[1]:

import requests
from datetime import datetime
from bs4 import BeautifulSoup
import io
import os
import time
import re
import xml.etree.cElementTree as ET
from random import randint


def crawl_1111(dire_para,rang,sect):
    j_dict={}
    err_ls=[]
    j_err_dict={}
    logtext=''
    date_crawl=datetime.today().strftime("%y%m%d")
    print datetime.today().strftime("%Y/%m/%d")+' start: '+datetime.now().strftime("%H:%M:%S")
    #1.1 從不同參數組合中抓取職缺列表(網址)
    target_wd=wdid[rang[0]:rang[1]]
    for p_j in jid:
        for p_wd in target_wd:

            #需要先抓一次以找到最高頁數
            get=0;times=0;max_pg=1;
            while get<1:
                try:
                    soup=getSoup('https://www.1111.com.tw/job-bank/job-index.asp?si=1&wc='+p_wd+'&d0='+p_j+'&fs=1&ps=100&page=1')
                    max_pg=int(soup.find('input','keypage')['data-tot'])
                    get+=1
                except requests.ConnectionError:
                    time.sleep(2+randint(1, 9)*0.1)
                    times+=1
                    print datetime.now().strftime("%H:%M:%S")+' :try '+str(times)+' times due to ConnectionError.'
                except:
                    time.sleep(2+randint(1, 9)*0.1)
                    times+=1
                    print datetime.now().strftime("%H:%M:%S")+' :try '+str(times)+' times due to other kinds of error.'

            for p_pg in range(1,(max_pg+1)):
                try:
                    url='https://www.1111.com.tw/job-bank/job-index.asp?si=1&wc='+p_wd+'&d0='+p_j+'&fs=1&ps=100&page='+str(p_pg)
                    soup=getSoup(url)
                except requests.ConnectionError:  
                    err_ls.append(url)
                    print datetime.now().strftime("%H:%M:%S")+' :ConnectionError Occured when retrieving job list'
                    time.sleep(4+randint(1, 9)*0.1)
                except:
                    err_ls.append(url)
                    print datetime.now().strftime("%H:%M:%S")+' : Other Error Occured when retrieving job list'
                    time.sleep(4+randint(1, 9)*0.1) 

                #從每一頁中存出職缺網址, 公司名稱, 職務名稱
                for item in soup.find_all('li','digest'):
                    j_dict['http:'+item.find('h3').find('a')['href']]=[item.find('span',itemprop='name').text,
                                                                       item.find('h3').find('a').text]
        print datetime.now().strftime("%H:%M:%S")+' :Category '+str(p_j)+' finished.'
    
    text='1-1: '+str(len(err_ls))+' page of list failed to crawl'
    print text;logtext+=text+'\r\n'
    
    ##1.2 爬失敗的頁數
    for url in err_ls:
        get=0;times=0
        while get<1:
            try:
                soup=getSoup(url)
                get+=1
            except:
                time.sleep(1+randint(1, 9)*0.1)
                times+=1
                print str(datetime.today())+' :try '+str(times)+' times while crawl '+url

        for item in soup.find_all('li','digest'):
            j_dict['http:'+item.find('h3').find('a')['href']]=[item.find('span',itemprop='name').text,
                                                                        item.find('h3').find('a').text]
    print '1-2 '+datetime.now().strftime("%H:%M:%S")+' '+str(len(err_ls))+' page of list saved'
    ##
    
    #2.1 存檔xml
    root=ET.Element('ls')
    root.set('Date',date_crawl)
    root.set('ITEM_COUNT','0')

    text=str(len(j_dict))+' URL were found. '+datetime.now().strftime("%H:%M:%S")
    logtext+=text+'\r\n';print text
    
    for key,value in j_dict.items():
        try:
            soup=getSoup(key)

            ic=int(root.get('ITEM_COUNT'))
            root.append(xml_element_generate(soup,key,value))
            root.set('ITEM_COUNT',str(ic+1))

            if ic%100==0:
                time.sleep(1)
            if ic%1000==0:
                text=datetime.now().strftime("%H:%M:%S")+' : '+str(ic)+'/'+str(len(j_dict))+' jobs downloaded'
                print text;logtext+=text+'\r\n'
        except requests.ConnectionError:  
            j_err_dict[key]=[value[0],value[1]]
            text=datetime.now().strftime("%H:%M:%S")+' :ConnectionError occured when saving job '+str(key)
            print text;logtext+=text+'\r\n'
            time.sleep(2+randint(1, 9)*0.1)
        except:
            j_err_dict[key]=[value[0],value[1]]
            text=datetime.now().strftime("%H:%M:%S")+' : Other types of error occurred when saving job '+str(key)
            print text;logtext+=text+'\r\n'
            time.sleep(2)

    text='2-1: '+datetime.now().strftime("%H:%M:%S")+' '+root.get('ITEM_COUNT')+' jobs data were crawled.  '
    print text;logtext+='\r\n\r\n'+text+'\r\n'
    text=str(len(j_err_dict))+' jobs faied to crawled in 2-1'
    print text;logtext+=text+'\r\n'
    
    #2.2 重新抓2.1發生錯誤的部分
    i=0
    for key,value in j_err_dict.items():
        get=0
        while get<1:
            try:
                soup=getSoup(key)

                ic=int(root.get('ITEM_COUNT'))
                root.append(xml_element_generate(soup,key,value))
                root.set('ITEM_COUNT',str(ic+1))

                if ic%100==0:
                    time.sleep(1)
                i+=1
                get+=1
            except:
                text='Error still occured in '+value[0]+value[1]+key
                time.sleep(5+randint(1, 9)*0.1)
                print text;logtext+=text+'\r\n'
            
    text=str(i)+' job saved after retry'
    print text;logtext+='\r\n'+text+'\r\n'
    print datetime.today().strftime("%Y/%m/%d")+' finish: '+datetime.now().strftime("%H:%M:%S")

    tree=ET.ElementTree(root)
    tree.write(open(dire_para+date_crawl+'_'+str(sect)+'.xml','wb'), encoding="utf-8")
    return logtext

