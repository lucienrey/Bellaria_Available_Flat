import json
import os
from utils import get_df, table_to_html, send_email

url = 'https://bellaria-zuerich.ch/angebot/'

def lambda_handler(event, context):
    df = get_df(url)
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
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }
lambda_handler(event=None,context=None)