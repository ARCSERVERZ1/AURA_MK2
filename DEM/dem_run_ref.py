# ranks updated 2023-09-06
import time
import time as t
import imaplib, email
from datetime import datetime
import pytz
import re
import pandas as pd
import math
import requests

url = 'http://127.0.0.1:8000/dem/datalogdem/'

# url = 'http://snju19.pythonanywhere.com/datalog/'

# url = 'http://aura19.pythonanywhere.com/datalog/'

# user = 'avinashbaswa.a4@gmail.com'
# password = 'kdoo tsqj ivrr sltu'

UserDetails = {'Sanjay': ['baswasanjay19@gmail.com', 'cntc yeac sblf jhdb'], }
               # 'Avinash': ['avinashbaswa.a4@gmail.com', 'vnjc iyfw skrm mcic'],
               # 'Veera': ['veeravalavanvi@gmail.com', 'znos kolx yyvj jkhk'],
               # 'lakshman': ['lakshman3b3@gmail.com', 'hmdq nokd bfxv ixjl']
               # }

df = pd.read_csv('rank.csv')
imap_url = 'imap.gmail.com'
date = '2023-11-18'
Debt_record = {}
Confusion_flag = 0
P_data = []
Confusion_text = '**'
budget = 0
UTC = pytz.utc
IST = pytz.timezone('Asia/Kolkata')
timestamp = str((datetime.now(IST))).split('.')
Total_sent, Total_recev, html_c, plain_c, dummy, Temp_Debt = 0, 0, 0, 0, 0, 0

Category = {":": "Bills&Payments", "!": "Entertainment", "@": "Food&Drinks", "*": "Kitchen&Grocery", '#': "Shoppings",
            "Travel": "Travel", 'medical': "Medicals", '[': "Debt", "-": "Skip", "danger": "extra", "play": "Play",
            "home": "Home", ']': "investment"}

Category_AD = {}
for i in (df.columns).tolist():
    Category_AD[i] = []
    for j in range(df.shape[0]):
        x = df.loc[j, i]
        if str(x) != 'nan':
            Category_AD[i].append(x.lower())
print(Category_AD)
if date == "":
    today = t.strftime('%Y-%m-%d')
    maildate = today
    x = datetime.strptime(today, '%Y-%m-%d')
    date = x.strftime('%d-%b-%Y')
else:
    x = datetime.strptime(date, '%Y-%m-%d')
    maildate = str(str(x).split(' ')[0])
    date = x.strftime('%d-%b-%Y')
print(date.split('-'))


def Get_raw_mail_data(user, password):
    html_mail = []
    plain_mail = []
    conn = imaplib.IMAP4_SSL(imap_url)
    conn.login(user, password)
    conn.select('Inbox')
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
                    html = email_message['text/html'].replace("  ", "").replace("\xa0", "").replace("\r", "").replace(
                        "\n", "").replace("\t", "")
                    html_mail.append(html.lstrip())
        if 'text/plain' in email_message:
            lenof = email_message['text/plain'].find('Hi')  # Cheers! ,Txn. ID
            x = email_message['text/plain'][:lenof].replace("  ", "").replace("\xa0", "").replace("\r", "").replace(
                "\n", "").replace("\t", "")
            plain_mail.append(x.lstrip())
    return plain_mail, html_mail


def Plain_details(string, type):
    global plain_c
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
        plain_c = plain_c + 1
        paid_to = str(string[lr3 + 13:l1])
        message = ''
        From_Bank = string[lr6 + 13:l5 + 4]

    elif type == 'Sent':
        plain_c = plain_c + 1
        paid_to = str(string[l3 + 7:l1])
        # date = str(string[:l3])
        From_Bank = string[l6 + 13:l5 + 4]
        message = str(string[l4 + 8:])
    elif type == 'Recharge':
        plain_c = plain_c + 1
        From_Bank = string[l6 + 25:l5 + 4]
        paid_to = string[lp3 + 12:l1]
        message = string[lp4 + 15:]

    Details = [type, money, paid_to, From_Bank, message]
    return Details


def html_details(x, type):
    global html_c
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
        html_c = html_c + 1

        message = str(x)[z5 + 258:z6 - 59]

    Details = [type, float(money), paid_to, From_Bank, message]
    return Details


def Get_Cat(data):
    global Category_money, Total_sent, Total_recev, plain_c, budget, dummy, Temp_Debt
    Temp_Debt = 0
    if data[0] == 'Sent' or data[0] == 'Recharge':

        # if data[4].find('%') != -1:
        #     print("Special_Mode")
        #     budget = budget + int(data[1])
        # if data[4].find('~') != -1:
        #     print("choose to Skip")
        #     data.append("Skip")
        #     return data
        AD = 0
        if data[4] != '':  # get category by message
            for i in Category:
                if data[4].find(i) != -1:
                    AD = 1
                    data.append(Category[i])
                    return data
        if AD == 0:  # get details by Auto detection
            Key = ((data[2] + data[4]).lower()).strip()

            # print(Key)
            for i in Category_AD:
                for j in Category_AD[i]:
                    if Key.find(j) != -1:
                        data.append(i)
                        return data
            else:
                data.append("Others")
                return data
    elif data[0] == 'Received':
        dummy = dummy + 1
        data.append("Received_NC")
        Total_recev = Total_recev + int(data[1])
        return data


# ----------------------------------------------------------------------------------------------------------------------
print("-------------------------------------------- B4 Operations ----------------------------------------------------")
# ----------------------------------------------------------------------------------------------------------------------
# Flow
for u in UserDetails:
    P_data = []
    print(UserDetails[u][0], UserDetails[u][1])

    plain_mail, html_mail = Get_raw_mail_data(UserDetails[u][0], UserDetails[u][1])

    for x in plain_mail:
        if x.find("Paid to") != -1:
            type = "Sent"
            P_data.append(Plain_details(x, type))
        elif x.find("Received from") != -1:
            type = "Received"
            P_data.append(Plain_details(x, type))
        elif x.find("Payment For") != -1:
            type = "Recharge"
            P_data.append(Plain_details(x, type))
        else:
            pass

    for x in html_mail:
        if x.find('Paid to') != -1:
            P_data.append(html_details(x, "Sent"))
        elif x.find('Received from') != -1:
            P_data.append(html_details(x, "Received"))

    Cate_data = []
    for i in P_data:
        Cate_data.append(Get_Cat(i))

    for i in Cate_data:

        try:
            data_template = {
                "date": maildate,
                "user": u,
                "type": i[0],
                "amount": int(i[1]),
                "sentFrom": i[3] if len(i[3]) < 50 not in [' ', ''] else 'from error',
                "sentTo": i[2] if len(i[2]) < 50 not in [' ', ''] else 'To error',
                "message": i[4] if i[4] not in [' ', ''] else 'No Message',
                "primaryCat": i[5],
                "groupCat": i[5]
            }

            status = requests.post(url, json=data_template)

            print(status.json())

            # print(data_template)


        except:
            print("Error for date :", i)

    print("#---------------------------------------------------------")
