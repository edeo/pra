import datetime
import os
import pycurl
import requests

import os 
from lxml import etree
import pandas as pd 
import datetime
import requests
from bs4 import BeautifulSoup
import time

dol_agency_codes = [
1220,
1225,
1205,
1219,
1218,
1250,
1245,
1240,
1293,
1290,
1235,
1210]


# find in the current inventory file

def inventory_file_name():
    today_xml_file_name = datetime.datetime.now().strftime('%Y-%m-%d_inventory.xml') 
    daily_inventory = '/home/jupyter-ed/projects/pra/data/inventory'
    os.chdir(daily_inventory)
    files=[]
    for file in os.listdir():
        if file.endswith(".xml"):
            files.append(file)

    if today_xml_file_name in files:
        return(today_xml_file_name)
    else:
        print("no inventory file available for today, go run data ingest file")

        
        
def get_xpath_strings(dol_agency_codes):       
    xpath_strings = []
    xpath_string_prefix = '//InformationCollectionRequest[.//AgencyCode/text()[. = "'
    xpath_string_suffix = '"]]'
    
    for number in dol_agency_codes:
        new_string = xpath_string_prefix+str(number)+xpath_string_suffix
        xpath_strings.append(new_string) 
    
    return(xpath_strings)
    
    
# create the list of omb control numbers



def inventory_to_omb_cntrl_number_list(file,dol_xpath_strings):
    tree = etree.parse(file)
    root = tree.getroot()
    omb_cntrl_number_list = []
    for string in dol_xpath_strings:
        req = root.xpath(string)
        for request in req:
            omb_cntrl_number_list.append(request.xpath('./OMBControlNumber//text()')[0])
    return(omb_cntrl_number_list)  


# generate the list of links
def history_table_link_generator(omb_control_number):
    reg_info_slug = "https://www.reginfo.gov/public/do/PRAOMBHistory?ombControlNumber="
    reg_info_url = reg_info_slug + omb_control_number
    return(reg_info_url)
  
    
def history_link_list_creator(omb_cntrl_number_list):
    omb_history_url_list = []
    for number in omb_cntrl_number_list:
        reg_info_url = history_table_link_generator(number)
        omb_history_url_list.append(reg_info_url)    
    return(omb_history_url_list)
    
# create the new folder for the days html files

def create_history_html_folder():
    folder_name = datetime.datetime.now().strftime('history_folder_%Y-%m-%d')   
    os.chdir('/home/jupyter-ed/projects/pra/data/history')
    # define the name of the directory to be created
    os.mkdir(folder_name)
    os.chdir(folder_name)
     
# download all the files to the folder
def get_history_html_file(praurl,omb_control_number):
    filename = omb_control_number +'.html'    
    file = open(filename,'wb')
    crl = pycurl.Curl()
    crl.setopt(crl.URL, praurl)
    crl.setopt(crl.WRITEDATA, file)
    crl.perform()
    crl.close()

def hmtl_down_from_cntrl_number_list(omb_cntrl_number_list,omb_history_url_list):
    list_range = range(len(omb_cntrl_number_list))
    for number in list_range:
        omb_cntrl_instance = omb_cntrl_number_list[number]
        praurl = omb_history_url_list[number]
        get_history_html_file(praurl,omb_cntrl_instance) 
        time.sleep(1)
    
    
    
   
    
file = inventory_file_name()
 
dol_xpath_strings = get_xpath_strings(dol_agency_codes)


omb_cntrl_number_list = inventory_to_omb_cntrl_number_list(file,dol_xpath_strings)
    
    
omb_history_url_list = history_link_list_creator(omb_cntrl_number_list)   
    
print('url list created')

print(os.getcwd)     
create_history_html_folder()    
print(os.getcwd)      
    
    
hmtl_down_from_cntrl_number_list(omb_cntrl_number_list,omb_history_url_list)    

print('html files downloaded') 
    
    
    
    
    
    
    
    