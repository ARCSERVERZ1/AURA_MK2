import os, json, re
import time as t
import imaplib, email
from datetime import datetime
import pytz, requests
from email.header import decode_header
import csvlogs

conn = imaplib.IMAP4_SSL('imap.gmail.com')
email_id = 'baswasanjay19@gmail.com'
password = 'cntc yeac sblf jhdb'
# email_id = 'avinashbaswa.a4@gmail.com'
# password = 'vnjc iyfw skrm mcic'
conn.login(email_id, password)
conn.select('Inbox')
date = '2024-08-02'

logs = csvlogs.start_logging('Avinash_DEM', os.getcwd())


def run(date):
    type = ''
    x = datetime.strptime(date, '%Y-%m-%d')
    mail_date = x.strftime('%d-%b-%Y')
    result, data = conn.search(None, '(FROM {0} ON {1})'.format("noreply@phonepe.com", mail_date))
    for Tmails, i in enumerate(data[0].split()):
        typ, data = conn.fetch(i, '(RFC822)')

        email_message = {
            part.get_content_type(): part.get_payload()
            for part in email.message_from_bytes((data[0][1])).walk()
        }
        for i in email_message:
            if i == 'text/html':
                mail_string = email_message['text/html'].replace("=", "").replace("  ", "").replace("\xa0", "").replace(
                    "\r", "").replace("\n", "").replace("\t", "")
                pattern = r'<[^>]*>'
                remove_html = re.sub(pattern, '', mail_string)
                cleaned_text = re.sub(r'\s+', ' ', remove_html).replace('E282B9', 'Rs').replace('&#8377;', 'Rs').strip()

                patter_paid_to = 'Paid to (.*?) Rs (\d+).*?from : (.*?)Bank.*? Message :(.*?)Hi'
                patter_payment = 'Payment For (\S+) Rs(\d+).*?XX(.*?)'

                final_match = re.search(patter_paid_to, cleaned_text)
                if final_match is None:
                    final_match = re.search(patter_payment, cleaned_text)
                try:
                    print(final_match.groups())
                    strg = ''
                    for match in final_match.groups():
                        strg = strg + str(match) + ' '
                    logs.datalog(type, 'OK', cleaned_text, strg)
                except:
                    print("Error-------------------------")
                    logs.datalog(type, 'NOK', cleaned_text, '')


for i in range(1, 9):
    date = '2024-08-'
    run('2024-08-07')
