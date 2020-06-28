import pycurl
import requests
import os 
from lxml import etree
import pandas as pd 
import datetime
import requests
from bs4 import BeautifulSoup
import json

def get_daily_inventory():
  url = 'https://www.reginfo.gov/public/do/PRAXML?type=inventory'
  r = requests.get(url)
  xml_file_name = datetime.datetime.now().strftime('%Y-%m-%d_inventory.xml')
  
  with open(xml_file_name, 'wb') as f:
    f.write(r.content)
    
  return(xml_file_name)



def get_daily_pending():
  url = 'https://www.reginfo.gov/public/do/PRAXML?type=pending'
  r = requests.get(url)
  xml_file_name = datetime.datetime.now().strftime('%Y-%m-%d_pending.xml')
  
  with open(xml_file_name, 'wb') as f:
    f.write(r.content)
    
  return(xml_file_name)


def get_daily_concluded():
  url = 'https://www.reginfo.gov/public/do/PRAXML?type=concluded'
  r = requests.get(url)
  xml_file_name = datetime.datetime.now().strftime('%Y-%m-%d_concluded.xml')
  
  with open(xml_file_name, 'wb') as f:
    f.write(r.content)
    
  return(xml_file_name)


def get_daily_expiration():
  url = 'https://www.reginfo.gov/public/do/PRAXML?type=expiration'
  r = requests.get(url)
  xml_file_name = datetime.datetime.now().strftime('%Y-%m-%d_concluded.xml')
  
  with open(xml_file_name, 'wb') as f:
    f.write(r.content)
    
  return(xml_file_name)


def todays_frn_link():
    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')
    prefix = "https://www.federalregister.gov/api/v1/documents.json?conditions%5Bagencies%5D%5B%5D=labor-department&conditions%5Bpublication_date%5D%5Bis%5D="
    spacer="%2F"
    conditions= "&conditions%5Btype%5D%5B%5D=NOTICE"
    query_url = prefix + str(month) + spacer + str(day) + spacer + str(year)
    return(query_url)




def get_frn_todays_frn(query_url):
    fr_request = requests.get(query_url)
    fr_json = fr_request.json()
    json_file_name = datetime.datetime.now().strftime('%Y-%m-%d_notices.json')
    with open(json_file_name, 'w') as f:
        json.dump(fr_json, f)


homepath = '/home/jupyter-ed/projects/pra'

os.chdir(homepath)

os.chdir('data/inventory')

get_daily_inventory()

os.chdir('../pending')

get_daily_pending()

os.chdir('../concluded')

get_daily_concluded()

os.chdir('../notices')
query_url = todays_frn_link()
get_frn_todays_frn(query_url)











