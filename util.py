
# coding: utf-8

# In[ ]:

import requests
from datetime import datetime
from bs4 import BeautifulSoup
import bs4
import io
import os
import time
import re
import xml.etree.cElementTree as ET
from random import randint


###參數組合
jid=['100100','100200','100300',     '110100','110200','110300',     '120100','120200','120300','120400',
     '130100','130200',     '140100','140200','140300','140400',     '150100','150200',
     '160100','160200','160300',     '170100','170200','170300',     '180100','180200','180300',
     '190100','190200',     '200100','200200','200300','200400',     '210100','210200',
     '220100','220200','220300','220400',     '230100','230200',     '240100','240200',
     '250100','250200','250300','250400','250500',     '260100','260200','260300',
     '270100','270200','270300',     '280100','280200',     '290100','290200']

wdid=['100100','100200','100300','100500','100600','100700','100800','100900','101100','101200',
      '101300','101400','101500','101600','101800','102000','100400','102100','102200','102300',
      '102400','102500','110000','120000','130000','140000','150000','160000']


def getSoup(url):
    res=requests.get(url,timeout=30)
    res.encoding='utf-8'
    return BeautifulSoup(res.text,"html5lib")

#處理非法字元
def xml_string_rep(text):
    text=re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",text)
    return re.sub('"','&quot;',re.sub('\'','&apos;',re.sub('&','&amp;',re.sub('<','&lt;',re.sub('>','&gt;', text)))))

def xml_element_generate(soup,key,value):
    #分別需要對工作內容、工作更新日期、以及職務條件作html解析以及存取
    
    item_node=ET.Element('ITEM')
    item_node.set(u'公司名稱',xml_string_rep(value[0]))
    item_node.set(u'職務名稱',xml_string_rep(value[1]))
    item_node.set(u'URL',key) #1/2新增
    
    for item in soup.find_all('li','paddingLB'):
        descrip=''
        for it in item.find_all('p'):
            descrip+=it.text+'\r\n'
        item_node.set(u'工作內容',xml_string_rep(descrip))

    for item in soup.find_all('span','update'):
        tmp=[]
        for st in item.strings:
            tmp.append(st)
        item_node.set(u'更新日期',xml_string_rep(re.sub(u'更新日期：','',tmp[0])))
    for item in soup.find_all('dd','tabarea'):
        tmp=''
        for tg in item.find_all('a',target="_blank"):
            tmp+=tg.text+u'\r\n'
        item_node.set(u'工作福利',xml_string_rep(tmp))
    for item in soup.find_all('li'):
        if item.find('div','listTitle')!=None:

            titl=item.find('div','listTitle').text
            
            if re.search(u'職務類別：',titl):
                job_category=u''
                for i in item.find_all('div','category'):
                    for ct in i.contents:
                        if type(ct)==bs4.element.NavigableString:
                            job_category+=ct+u','
                item_node.set(re.sub(u'：','',titl),xml_string_rep(job_category))
            elif re.search(u'科系限制：',titl):
                for i in item.find_all('div','listContent'):
                    tmp=''
                    for st in i.strings:
                        tmp+=st
                    item_node.set(u'科系限制',xml_string_rep(tmp))
            else:
                for i in item.find_all('div','listContent'):
                    tmp=''
                    for ch in i.children:
                        if type(ch)==bs4.element.NavigableString:
                            tmp+=ch+u'\r\n'
                    item_node.set(re.sub(u'：','',titl),xml_string_rep(unicode(tmp)))
    return item_node

