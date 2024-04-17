# ranks updated 2023-09-06
import time
import time as t
import imaplib, email
from datetime import datetime
import pytz
import re, json
import pandas as pd
import math
import requests
from email.header import decode_header
import os




def axis_bank_message_to_schema(message):
    axis_credit_transaction_schema = []
    for i in message:
        schema = ['Sent', '', 'Axis_Credit']
        match = re.search(r'Card no. (.*?) for INR (\d+) at\s+(.*?)\s+In', i)
        if match:
            schema.insert(1, match.group(2))
            schema.insert(2, match.group(3))
            schema.insert(3, match.group(1))
            axis_credit_transaction_schema.append(schema)
        return axis_credit_transaction_schema
    return []


def get_all_transactions(conn, date, platforms):
    phone_pe_transactions = []
    axis_bank_schema = []

    if 'Phone_pe' in platforms:
        html_mail = []
        plain_mail = []

        result, data = conn.search(None, '(FROM {0} ON {1})'.format("noreply@phonepe.com", date))

        for Tmails, i in enumerate(data[0].split()):
            typ, data = conn.fetch(i, '(RFC822)')
            email_message = {
                part.get_content_type(): part.get_payload()
                for part in email.message_from_bytes((data[0][1])).walk()
            }
            for mail in email_message:
                if mail == 'multipart/mixed':
                    if 'text/html' in email_message:
                        html = email_message['text/html'].replace("  ", "").replace("\xa0", "").replace("\r",
                                                                                                        "").replace(
                            "\n", "").replace("\t", "")
                        html_mail.append(html.lstrip())
            if 'text/plain' in email_message:
                lenof = email_message['text/plain'].find('Hi')  # Cheers! ,Txn. ID
                x = email_message['text/plain'][:lenof].replace("  ", "").replace("\xa0", "").replace("\r",
                                                                                                      "").replace(
                    "\n", "").replace("\t", "")
                plain_mail.append(x.lstrip())

        for x in plain_mail:
            if x.find("Paid to") != -1:
                phone_pe_transactions.append(phone_pe_plain_mail_details(x, "Sent"))
            elif x.find("Received from") != -1:
                phone_pe_transactions.append(phone_pe_plain_mail_details(x, 'Received'))
            elif x.find("Payment For") != -1:
                phone_pe_transactions.append(phone_pe_plain_mail_details(x, 'Recharge'))
            else:
                pass
        for x in html_mail:
            if x.find('Paid to') != -1:
                phone_pe_transactions.append(phone_pe_html_mail_details(x, "Sent"))
            elif x.find('Received from') != -1:
                phone_pe_transactions.append(phone_pe_html_mail_details(x, "Received"))
        # print(phone_pe_transactions)

    if 'Axis_credit' in platforms:
        result, message = conn.search(None, '(FROM {0} ON {1})'.format("alerts@axisbank.com", date))
        transaction_msg_list = []
        for num in message[0].split():
            _, msg_data = conn.fetch(num, "(RFC822)")
            raw_mail = msg_data[0][1]
            msg = email.message_from_bytes(raw_mail)
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            # print(subject)
            if subject.find('Transaction alert on Axis Bank Credit Card no') != 1:
                ref = str(msg).find('</span> <br><br>')
                transaction_msg = str(str(msg)[ref + 82:ref + 82 + 185])
                transaction_msg.replace("=\\n", 'x')
                transaction_msg_list.append(transaction_msg)

        axis_bank_schema = axis_bank_message_to_schema(transaction_msg_list)

        # print(axis_bank_schema)
        # for i in (phone_pe_transactions + axis_bank_schema):
        #     print(i)

    return phone_pe_transactions + axis_bank_schema


def phone_pe_html_mail_details(x, type):
    KeyWords = ['block">', '</span> </td>', '=E2=82=B9', 'End of User name', '> Message', 'End of '
                                                                                          'Message',
                'Credited to', 'End of Bank Account']

    z1 = str(x).find(KeyWords[0])
    z2 = str(x).find(KeyWords[1])
    z3 = str(x).find(KeyWords[2])
    z4 = str(x).find(KeyWords[3])
    z5 = str(x).find(KeyWords[4])
    z6 = str(x).find(KeyWords[5])
    z7 = str(x).find(KeyWords[6])
    z8 = str(x).find(KeyWords[7])
    paid_to = str(x)[z1 + 8:z2]
    money = str(x)[z3 + 9:z4 - 58]
    try:
        money = float(money)
    except:
        try:
            int_value = [int(s) for s in money.split() if s.isdigit()]
            money = float(int_value[0])
        except:
            float_value = re.findall("\d+\.\d+", money)
            money = float(float_value[0])

    message = ''
    From_Bank = str(x)[z8 - 47:z8 - 26]
    if type != 'Received':
        message = str(x)[z5 + 258:z6 - 59]

    Details = [type, float(money), paid_to, From_Bank, message, 'Phonepe']
    print("html", Details)
    return Details


def phone_pe_plain_mail_details(string, type):
    l1 = string.find('₹')
    l2 = string.find('Txn')
    l3 = string.find('Paid to')
    lr3 = string.find('Received from')
    lp3 = string.find('Payment For')
    l4 = string.find('Message')
    lp4 = string.find('MobileProvider')
    l5 = string.find('Bank')
    l6 = string.find('Debited')
    lr6 = string.find('Credited')
    money = float(string[l1 + 1:l2])
    message = '**NOT DEFINED'
    paid_to = '**NOT DEFINED'
    From_Bank = '**NOT DEFINED'
    # print(l6)
    # print("Debited" , string)
    if type == 'Received':
        paid_to = str(string[lr3 + 13:l1])
        message = ''
        From_Bank = string[lr6 + 13:l5 + 4]

    elif type == 'Sent':
        paid_to = str(string[l3 + 7:l1])
        # date = str(string[:l3])
        From_Bank = string[l6 + 13:l5 + 4]
        message = str(string[l4 + 8:])
    elif type == 'Recharge':
        From_Bank = string[l6 + 25:l5 + 4]
        paid_to = string[lp3 + 12:l1]
        message = string[lp4 + 15:]

    Details = [type, money, paid_to, From_Bank, message, 'Phonepe']
    return Details


class GetSpendings:
    def __init__(self, user, platforms=(), date="", url='https://serveraura.pythonanywhere.com/dem/datalogdem/'):
        self.user = user
        self.pass_date = date
        self.platforms = platforms
        self.url = url
        print(os.getcwd())
        self.user_data = json.loads(open('user_data.json').read())
        self.imap_url = 'imap.gmail.com'
        self.ist_time = datetime.now(pytz.timezone('Asia/Kolkata'))
        self.date = self.pass_date
        if self.date == "":
            self.today = t.strftime('%Y-%m-%d')
            self.maildate = self.today
            x = datetime.strptime(self.today, '%Y-%m-%d')
            self.date = x.strftime('%d-%b-%Y')
        else:
            x = datetime.strptime(self.date, '%Y-%m-%d')
            self.maildate = str(str(x).split(' ')[0])
            self.date = x.strftime('%d-%b-%Y')
        print("-----------------------------------------DEM_MK2 - run.py initialized for date {date}".format(
            date=self.date))

    def categorise_transactions(self, all_transactions):
        AUTO_CAT = json.loads(open('auto_categorisation.json').read())
        GET_GROUP = json.loads(open('group_data.json').read())
        # check group
        for transactions in all_transactions:
            # print("This one",transactions)
            match = re.search(r'#(\w+)(\d+)#', transactions[4])
            if match:
                if int(match.group(2)) == 1:
                    GET_GROUP[self.user] = [
                        # str(self.ist_time.day)+str(self.ist_time.month) + str(self.ist_time.year % 100) + '|' +
                        # str(match.group(1)),
                        str(self.pass_date.split('-')[0])[2:] + str(self.pass_date.split('-')[1]) + str(
                            self.pass_date.split('-')[2]) + '|' + str(match.group(1)),

                        self.pass_date]
                    with open('group_data.json', 'w') as json_file:
                        json.dump(GET_GROUP, json_file)
                else:
                    GET_GROUP[self.user] = ['NO_GROUP', '-']
                    with open('group_data.json', 'w') as json_file:
                        json.dump(GET_GROUP, json_file)
        if datetime.strptime(GET_GROUP[self.user][1], '%Y-%m-%d') <= datetime.strptime(self.pass_date, '%Y-%m-%d'):
            pass
            # print(f"{GET_GROUP[self.user][1]} > {datetime.strptime(self.pass_date, '%Y-%m-%d')}")

        else:
            GET_GROUP[self.user] = ['NO_GROUP', '']
            # print(f"old data so update no group")

        # categorising
        for transactions in all_transactions:
            transactions.insert(5, transactions[4])
            transactions.insert(6, GET_GROUP[self.user][0])
            key_sentence = transactions[2] + ' ' + transactions[4]
            break_all = False
            for category in AUTO_CAT['auto_category']:
                if break_all: break
                if category == 'Others': transactions.insert(5, category)
                # special cases (debt)
                try:
                    match_debt = re.search(r'\[(\d+)\]', transactions[4])
                    if match_debt:
                        match_debt.group(1)
                        transactions.insert(5, 'DEBT-OUT')
                        break
                except:
                    pass
                # normal search
                for keyword in AUTO_CAT['auto_category'][category]:
                    match = re.search(r'\b' + re.escape(keyword) + r'\b', key_sentence, flags=re.IGNORECASE)
                    if match:
                        # print(f"Found the word '{keyword}' at for category {category}.")
                        transactions.insert(5, category)
                        break_all = True
                        break

        return all_transactions

    def send_data(self, final_data):
        count = 0

        for i in final_data:
            # print(i)
            count = count + 1
            data_template = {
                "user": i[0],
                "date": i[1],
                "transaction_type": i[2],
                "amount": int(i[3]),
                "sender_bank": i[5],
                "receiver_bank": i[4],
                "message": i[6] if i[6] not in [' ', ''] else 'No Message',
                "category": i[7],
                "sub_category": i[8] if i[8] not in [' ', ''] else 'NC',
                "group": i[9],
                "payment_method": i[10],
                "data_ts": i[11]
                # "xtra"
            }
            url = f'https://serveraura.pythonanywhere.com/dem/datalogdem/{count}/{i[0]}/{i[1]}'
            # url = f'http://127.0.0.1:8000/dem/datalogdem/{count}/{i[0]}/{i[1]}'
            status = requests.post(url, json=data_template)
            print(status.json())
        return True

    def get_all_transaction(self):
        if self.user in self.user_data["users"]:
            # connect to gmail
            conn = imaplib.IMAP4_SSL(self.imap_url)
            email_id = self.user_data['details'][self.user][0]
            password = self.user_data['details'][self.user][1]
            conn.login(email_id, password)
            conn.select('Inbox')
            all_transactions = get_all_transactions(conn, self.date, self.platforms)
            catergorised = self.categorise_transactions(all_transactions)
            for i in catergorised[:]:
                i.insert(0, self.user)
                i.insert(1, self.pass_date)
                formatted_time = self.ist_time.now().strftime("%Y-%m-%d %H:%M:%S")
                i.insert(11, formatted_time)

            self.send_data(catergorised)
        else:
            print("User name not in the user list")
            return ['Check user']


if __name__ == '__main__':
    # for i in range(1, 15):
    #     if len(str(i)) == 1:
    #         i = '0' + str(i)
    #     date = f'2024-01-{i}'
        # print(i)
        get = GetSpendings('avinash', ['Phone_pe', 'Axis_credit'], '2024-03-04', ).get_all_transaction()
    #     get = GetSpendings('sanjay', ['Phone_pe', 'Axis_credit'], '2023-12-10', ).get_all_transaction()
