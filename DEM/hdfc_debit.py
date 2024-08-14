import os, json, re
import time as t
import imaplib, email
from datetime import datetime
import pytz, requests
from email.header import decode_header

conn = imaplib.IMAP4_SSL('imap.gmail.com')
email_id = 'baswasanjay19@gmail.com'
password = 'cntc yeac sblf jhdb'

# email_id = 'avinashbaswa.a4@gmail.com'
# password = 'vnjc iyfw skrm mcic'

conn.login(email_id, password)
conn.select('Inbox')
pass_date = '2024-08-10'
x = datetime.strptime(pass_date, '%Y-%m-%d')
mail_date = x.strftime('%d-%b-%Y')

result, message = conn.search(None, '(FROM {0} ON {1})'.format("alerts@hdfcbank.net", mail_date))
transaction_msg_list = []
for num in message[0].split():
    _, msg_data = conn.fetch(num, "(RFC822)")
    raw_mail = msg_data[0][1]
    msg = email.message_from_bytes(raw_mail)
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")
    if subject.find('You have done a UPI txn. Check details!') != -1:
        ref = str(msg).find('Dear')
        transaction_msg = str(str(msg)[ref:ref + 329])
        transaction_msg = str(str(transaction_msg).replace("=\n", ''))

        pattern = r'Rs.(.*?)\..*?debited from account (.*?) to VPA (.*?) on'
        match = re.search(pattern, str(transaction_msg))

        if match is None:
            print(str(transaction_msg))
        else:
            print(match.groups())

