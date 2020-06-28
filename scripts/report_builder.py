# find the information, save as csv for rmarkdown to read later
import pycurl
import requests
import os 
from lxml import etree
import pandas as pd 
import datetime
import requests
from bs4 import BeautifulSoup
import json
import numpy as np



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

def get_xpath_strings(dol_agency_codes):       
    xpath_strings = []
    xpath_string_prefix = '//InformationCollectionRequest[.//AgencyCode/text()[. = "'
    xpath_string_suffix = '"]]'
    
    for number in dol_agency_codes:
        new_string = xpath_string_prefix+str(number)+xpath_string_suffix
        xpath_strings.append(new_string) 
    
    return(xpath_strings)
    

def inventory_to_list(file,dol_agency_codes):
    xpath_strings= get_xpath_strings(dol_agency_codes)
    
    tree = etree.parse(file)
    root = tree.getroot()
    all_results = []

    for string in xpath_strings:
      results = []
      req = root.xpath(string)
      for request in req:       
        try:
         results.append({
           "omb_control_number": request.xpath('./OMBControlNumber//text()')[0],
           "icr_reference_number": request.xpath('./ICRReferenceNumber//text()')[0],
           "Title": request.xpath('./Title//text()')[0],
           #"Abstract": request.xpath('./Abstract//text()')[0],
           "AgencyCode": str(request.xpath('./AgencyCode//text()')[0]).strip(),
           "ICRTypeCode": str(request.xpath('./ICRTypeCode//text()')[0]).strip(),
           "expiration_date": str(request.xpath('./Expiration/ExpirationDate//text()')[0]).strip(),
           "ICR_status": str(request.xpath('./ICRStatus//text()')[0]).strip()})
        except:
            results.append({
              "omb_control_number": request.xpath('./OMBControlNumber//text()')[0],
              "icr_reference_number": request.xpath('./ICRReferenceNumber//text()')[0],
              "Title": request.xpath('./Title//text()')[0],
              #"Abstract": request.xpath('./Abstract//text()')[0],
              "AgencyCode": str(request.xpath('./AgencyCode//text()')[0]).strip(),
              "ICRTypeCode": str(request.xpath('./ICRTypeCode//text()')[0]).strip(),
              "expiration_date": str(request.xpath('./Expiration/ExpirationDate//text()')[0]).strip(),
              "ICR_status": "None"})
            
      all_results.append(results) 
    return(all_results)
    
    
    
def inventory_list_to_table(file,all_results):    
    dol_inventory_row_list = []
    
    for list in all_results:
      for row in list:
        dol_inventory_row_list.append(row)
    
    dol_inventory_table = pd.DataFrame(dol_inventory_row_list)
    dol_inventory_table['file_date'] = file
    return(dol_inventory_table)    

def create_report_folder():
    folder_name = datetime.datetime.now().strftime('report_folder_%Y-%m-%d')   
    os.chdir('/home/jupyter-ed/projects/pra/reports')
    # define the name of the directory to be created
    os.mkdir(folder_name)
    return(folder_name)
    

           
           
           

           
           
           
           
# list all the files in the directory
files=[]
daily_inventory = '/home/jupyter-ed/projects/pra/data/inventory'
os.chdir(daily_inventory)

files = [] 

for file in os.listdir():
    if file.endswith(".xml"):
        files.append(file)


        
# turn the list of files into a data frame

df = pd.DataFrame(files,columns=['files'])

df = df.sort_values(by='files',ascending=False)


# get todays inventory file

today=str(df.iloc[0,0])
# get yesterdays inventory file
yesterday=str(df.iloc[1,0])

# create a dataframe from yesterdays file

yesterday_list  = inventory_to_list(yesterday,dol_agency_codes)           
yesterday_table = inventory_list_to_table(yesterday,yesterday_list)


# create a dataframe from todays file
today_list  = inventory_to_list(today,dol_agency_codes)           
today_table = inventory_list_to_table(today,today_list)


# create a list of  yesterdays icr numbers
yesterdays_list = list(yesterday_table['icr_reference_number'])
todays_list = list(today_table['icr_reference_number'])


new_today = list(np.setdiff1d(todays_list,yesterdays_list))
gone_today = list(np.setdiff1d(yesterdays_list,todays_list))



# create the tables

today_table['expiration_date'] = pd.to_datetime(today_table['expiration_date'])

new_in_inventory_today_table = today_table[today_table['icr_reference_number'].isin(new_today)]

gone_from_inventory_today_table = yesterday_table[yesterday_table['icr_reference_number'].isin(gone_today)]

expiring_soonest = today_table.sort_values(by='expiration_date',ascending=True).head(30)

# write out as csvs

report_folder=create_report_folder()
           
os.chdir(report_folder)

new_in_inventory_today_table.to_csv('new_in_inventory_today_table.csv')
gone_from_inventory_today_table.to_csv('gone_from_inventory_today_table.csv')
expiring_soonest.to_csv('expiring_soonest.csv')           
           
## pending
           
pending = '/home/jupyter-ed/projects/pra/data/pending'
output_folder = '/home/jupyter-ed/projects/pra/reports'+report_folder
print(output_folder)

def xml_file_difference(data_folder,output_folder):           
    
    os.chdir(data_folder)

    files = [] 
    for file in os.listdir():
        if file.endswith(".xml"):
            files.append(file)

# turn the list of files into a data frame

    df = pd.DataFrame(files,columns=['files'])

    df = df.sort_values(by='files',ascending=False)


    # get todays inventory file

    today=str(df.iloc[0,0])
    # get yesterdays inventory file
    yesterday=str(df.iloc[1,0])

    # create a dataframe from yesterdays file

    yesterday_list  = inventory_to_list(yesterday,dol_agency_codes)           
    yesterday_table = inventory_list_to_table(yesterday,yesterday_list)


    # create a dataframe from todays file
    today_list  = inventory_to_list(today,dol_agency_codes)           
    today_table = inventory_list_to_table(today,today_list)


    # create a list of  yesterdays icr numbers
    yesterdays_list = list(yesterday_table['icr_reference_number'])
    todays_list = list(today_table['icr_reference_number'])


    new_today = list(np.setdiff1d(todays_list,yesterdays_list))
    gone_today = list(np.setdiff1d(yesterdays_list,todays_list))

    new_in_inventory_today_table = today_table[today_table['icr_reference_number'].isin(new_today)]

    gone_from_inventory_today_table = yesterday_table[yesterday_table['icr_reference_number'].isin(gone_today)]

 
    os.chdir(output_folder)
    new_in_inventory_today_table.to_csv('new_in_pending_today_table.csv')
    gone_from_inventory_today_table.to_csv('gone_from_pending_today_table.csv')
    today_table.to_csv('pending.csv')
    return(print("done"))
           
 
           
           
           
xml_file_difference(pending,output_folder)           