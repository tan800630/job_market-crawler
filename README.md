# job_market-crawler

The present code is a web crawler targeting a famous job bank website, users can crawl job opening informations in different cities/region (e.g. parameter 1 represents Taipei City, whilst 2 denote New Taipei City. Correspendences between Cities/region and parameters will be upload in a few days.).

**!! The code could only be seen as a demo of how to crawl data with python. Any usage that might violate the law is not recommanded. !!**

## Prerequisites
- python 2.7

- requests
- beautifulsoup
- xml.etree.cElementTree

## Usage

Enter the following code in cmd

    python main.py dire_para="C:/Users/user/Documents" rang=16-17 sect=00 save=F

**dire_para**: directory/path that crawled data being saved. (dire_para would be set in current directory if the parameter is not specified)
**rang**: range of location parameters being crawler with python range() format. (e.g. "rang=0-1" equal to range(0,1). 17-18 is set as default. )
**sect**: suffix to be added on the filename. (99 is set as default)
**save**: if the log file should be saved (in the same directory). T means True, and F means False.
