import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests
import os
import json


def get_df(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # only free flat
    free_flat = soup.findAll(class_='frei')
    
    try:
        newdf = []
        for i in free_flat:
            flat_info = [each.text for each in i.findAll('td')]
            newdf.append(flat_info)
            
        flat_info = []
        for i in newdf:
            values = {'flat' : i[0],
                    'floor' : i[1],
                    'size' : i[2],
                    'squaredmeters' : i[3],
                    'price1' : i[4],
                    'price2' : i[5],
            }
            flat_info.append(values)
            
        final_list = []
        for i in flat_info:
            if i['size'] == '4.5':
                final_list.append(i)
        df = final_list

    except:
        print("Error: No possible to get the website content.")
        df = []
    
    return df

def table_to_html(jsonlist):
    new = "<tbody>\n"
    for i in jsonlist:
        new = new + "<tr>"
        for key, value in i.items():
            new = str(new) + "<td>" + str(value) + "</td>\n"
        new = new + "</tr>\n"
    new = new + "</tbody>"
    table = """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Flat</th>
      <th>Floor</th>
      <th>Size</th>
      <th>FloorSize</th>
      <th>Price</th>
      <th>NebenKosten</th>
    </tr>
  </thead>
  """ + new + """ </table>"""
    
    return table 


def send_email(subject, html_message, url):
    try:
        recipients = [os.environ.get('EMAIL_ADDRESS')] 
        #emaillist = ['lucienrey@hotmail.com','evgenia.gupalova@gmail.com'] 
        emaillist = ['lucienrey@hotmail.com']  
        msg = MIMEMultipart()
        msg['Subject'] = "Your Subject"
        msg['From'] = str(os.environ.get('EMAIL_ADDRESS'))

        part1 = MIMEText(html_message, 'html')
        msg.attach(part1)

        server = smtplib.SMTP('smtp.live.com', 587)
        server.ehlo()
        server.starttls()
        server.login(os.environ.get('EMAIL_ADDRESS'),os.environ.get('EMAIL_PASSWORD'))
        server.sendmail(msg['From'], emaillist , msg.as_string())
        print('Success: Email Sent to Users.')
    except:
        print('Error: Email Not Sent')