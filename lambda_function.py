import json
import os

from utils import get_df, table_to_html, send_email, get_json_s3, save_json_s3

url = 'https://bellaria-zuerich.ch/angebot/'

def lambda_handler(event, context):

    df = get_df(url)
    previous_df = get_json_s3('Flat_Available.json')
    if df == previous_df:
        return {
            'statusCode': 200,
            'body': json.dumps('Success - No Changes on The Website.'),
            'save_newfile' : False,
            'send_email' : False,
            'new_list' :df,
            'previous_list' :previous_df,
        }

    elif df == []:
        save_json_s3(df,'Flat_Available.json')

        return {
            'statusCode': 200,
            'body': json.dumps('Success - No Flats (3.5/Attika) Available At the moment!'),
            'save_newfile' : True,
            'send_email' : False,
            'new_list' :df,
            'previous_list' :previous_df,
        }

    else:
        html_table = table_to_html(df)
        subject = 'Bellaria - New Update'

        html_message = """\
        <html>
            <head></head>
            <body>
            Hi, the Bellaria website has been updated! Below the changes: <br><Br>
            {0}
            <br><br>
            Apply for the new flat here : <a href='""".format(html_table) + url + """'>Link</a> <br>
            Best of Luck! <Br> Lucien &#9829;
            </body>
        </html>
        """

        send_email(subject,html_message,url)

        save_json_s3(df,'Flat_Available.json')

        return {
            'statusCode': 200,
            'body': json.dumps('Success - New Flats -  Email Sent to User'),
            'save_newfile' : False,
            'send_email' : True,
            'new_list' :df,
            'previous_list' :previous_df,
        }

