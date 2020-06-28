# python file



import datetime 
from datetime import date, timedelta
import os
import pycurl
import requests

import os 
from lxml import etree
import pandas as pd 
import datetime
import requests
from bs4 import BeautifulSoup




def create_history_html_folder():
    folder_name = datetime.datetime.now().strftime('history_folder_%Y-%m-%d')   
    os.chdir('/home/jupyter-ed/projects/history')
    # define the name of the directory to be created
    os.mkdir(folder_name)
    return(folder_name)
    

def get_daily_inventory():
  url = 'https://www.reginfo.gov/public/do/PRAXML?type=inventory'
  r = requests.get(url)
  xml_file_name = datetime.datetime.now().strftime('%Y-%m-%d_inventory.xml')
  
  with open(xml_file_name, 'wb') as f:
    f.write(r.content)
    
  return(xml_file_name)

    

def inventory_to_omb_cntrl_number_list(file,dol_xpath_strings):
    tree = etree.parse(file)
    root = tree.getroot()
    omb_cntrl_number_list = []

    for string in xpath_strings:
      req = root.xpath(string)
      for request in req:
        omb_cntrl_number_list.append(request.xpath('./OMBControlNumber//text()')[0])
     
    return(omb_cntrl_number_list)  



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
    


def get_history_html_file(praurl,omb_control_number):
    filename = omb_control_number +'.html'    
    file = open(filename,'wb')
    crl = pycurl.Curl()
    crl.setopt(crl.URL, praurl)
    crl.setopt(crl.WRITEDATA, file)
    crl.perform()
    crl.close()

def hmtl_list_generator(omb_cntrl_number_list,omb_history_url_list):
    list_range = range(len(omb_cntrl_number_list))
    for number in list_range:
        omb_cntrl_instance = omb_cntrl_number_list[number]
        praurl = omb_history_url_list[number]
        get_history_html_file(praurl,omb_cntrl_instance)
        

def get_first_row_history(file):
    with open(file) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content] 
        omb_data = {"icr_ref_number" : content[778],
                    "request_type" : content[785].replace('&nbsp;',""),
                    "received_by_omb"  : content[788].replace('&nbsp;',""),
                    "conclusion_date"  : content[794].replace('&nbsp;',""),
                    "conclusion_action"  : content[798],
                    "omb_control_number": file[0:9]}
        return(omb_data)


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

xpath_strings = []

xpath_string_prefix = '//InformationCollectionRequest[.//AgencyCode/text()[. = "'
xpath_string_suffix = '"]]'

for number in dol_agency_codes:
    new_string = xpath_string_prefix+str(number)+xpath_string_suffix
    xpath_strings.append(new_string)  




        

todays_folder_name = create_history_html_folder()

os.chdir(todays_folder_name)


print('getting inventory')  
xml_file_name = get_daily_inventory()     

omb_cntrl_number_list = inventory_to_omb_cntrl_number_list(xml_file_name,xpath_strings)

omb_history_url_list = history_link_list_creator(omb_cntrl_number_list)

print('getting html')

hmtl_list_generator(omb_cntrl_number_list,omb_history_url_list)

rows = []

print('get first row')
for file in os.listdir():
    if file.endswith(".html"):
        data=get_first_row_history(file)
        rows.append(data)


row_range = range(len(rows))



for number  in row_range:
    try:
        rows[number]['icr_ref_number'] = rows[number]['icr_ref_number'].split('>')[1].split('<')[0]
    except:
        rows[number]['icr_ref_number'] = rows[number]['icr_ref_number']       


for number  in row_range:
    try:
        rows[number]['conclusion_action'] = rows[number]['conclusion_action'].split('>')[1].split('<')[0]
    except:
        rows[number]['conclusion_action'] = rows[number]['conclusion_action']   

print('history table')
history_table = pd.DataFrame(rows)


history_table['received_by_omb'] = pd.to_datetime(history_table['received_by_omb'])

history_table['conclusion_date'] = pd.to_datetime(history_table['conclusion_date'])

datetime.datetime.now().strftime('%Y-%m-%d_inventory.xml')

dt = date.today() - timedelta(5)

dt = dt.strftime('%Y-%m-%d')

filter_date = dt

mask = (history_table['received_by_omb'] > filter_date) | (history_table['conclusion_date'] > filter_date) 

week_table = history_table.loc[mask]
print('writeout')
week_table.to_csv('week_table_'+date.today().strftime('%Y-%m-%d')+'.csv')




