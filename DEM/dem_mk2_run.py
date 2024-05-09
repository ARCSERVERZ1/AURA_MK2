import os, json, re
import time as t
import imaplib, email
from datetime import datetime
import pytz , requests
from email.header import decode_header


def validation(text, type):
    if type == 'int':
        if text.isdigit():
            return [int(text), 0]
        else:
            return [0, 0]
    else:
        if len(text) > 30:
            return [str(text)[:30], 1]
        else:
            return [str(text), 0]


class GetSpendings:
    def __init__(self, user, platforms=(), date="", url='https://serveraura.pythonanywhere.com/dem/datalogdem/', post = True):
        self.all_transactions = []
        self.user = user
        self.pass_date = date
        self.platforms = platforms
        self.url = url
        self.imap_url = 'imap.gmail.com'
        self.ist_time = datetime.now(pytz.timezone('Asia/Kolkata'))
        self.post = post
        if self.pass_date == "":
            self.today = t.strftime('%Y-%m-%d')
            self.mail_date = datetime.strptime(self.today, '%Y-%m-%d').strftime('%d-%b-%Y')
            self.pass_date = self.today
        else:
            x = datetime.strptime(self.pass_date, '%Y-%m-%d')
            self.mail_date = x.strftime('%d-%b-%Y')
            self.pass_date = str(str(x).split(' ')[0])

        print( f"------------### Data log request for {self.user} for date {self.mail_date} ###---------------")
        try:
            self.user_data = json.loads(open('user_data.json').read())
            try:
                if self.user in self.user_data["users"]:
                    self.conn = imaplib.IMAP4_SSL('imap.gmail.com')
                    email_id = self.user_data['details'][self.user][0]
                    password = self.user_data['details'][self.user][1]
                    self.conn.login(email_id, password)
                    self.conn.select('Inbox')
                    self.get_all_transaction()
                else:
                    print(f'User name {self.user} not found ')
            except Exception as e:
                print("Error")
                print(e)
        except:
            print(f"Json Error in directory {os.getcwd()}")

    def get_all_transaction(self):

        if 'phone_pe' in self.platforms: self.run_phone_pe_log()
        if 'axis_credit' in self.platforms: self.run_axis_credit_log()

        for transaction in self.all_transactions:
            self.get_categorised(transaction)
        self.datalog()

    def run_phone_pe_log(self):

        result, data = self.conn.search(None, '(FROM {0} ON {1})'.format("noreply@phonepe.com", self.mail_date))
        for Tmails, i in enumerate(data[0].split()):
            typ, data = self.conn.fetch(i, '(RFC822)')

            email_message = {
                part.get_content_type(): part.get_payload()
                for part in email.message_from_bytes((data[0][1])).walk()
            }

            for i in email_message:
                if i == 'text/html':
                    mail_string = email_message['text/html'].replace("=", "").replace("  ", "").replace("\xa0",
                                                                                                        "").replace(
                        "\r", "").replace("\n", "").replace("\t", "")

                    receiver = mail_string[mail_string.find('<!-- User name / Amount -->') + 550: mail_string.find(
                        '<!-- End of User name / Amount -->') - 250].replace('/', '').replace('<', '').strip()

                    amount = mail_string[mail_string.find('&#8377;') + 8: mail_string.find(
                        '<!-- End of User name / Amount -->') - 31].replace('/', '').replace('<', '').strip()

                    sender = mail_string[mail_string.find('<!-- Bank Account -->') + 395: mail_string.find(
                        '<!-- End of Bank Account -->') - 15].replace('/', '').replace('<', '').strip()
                    message = mail_string[mail_string.find('<!-- Message -->') + 550: mail_string.find(
                        '<!-- End of Message -->') - 32].replace('/', '').replace('<', '').strip()

                    receiver = validation(receiver, 'text')
                    sender = validation(sender, 'text')
                    message = validation(message, 'text')
                    amount = validation(amount, 'int')

                    anamoaly = receiver[1] + sender[1] + message[1] + amount[1] if receiver[1] + sender[1] + message[
                        1] + amount[1] > 0 else 0

                    if amount[0] == 0 and anamoaly > 1:
                        pass
                    else:
                        self.all_transactions.append(
                            [self.user ,'sent', amount[0], receiver[0], sender[0], message[0], 'phone_pe', anamoaly])

    def run_axis_credit_log(self):

        result, message = self.conn.search(None, '(FROM {0} ON {1})'.format("alerts@axisbank.com", self.mail_date))
        transaction_msg_list = []
        for num in message[0].split():

            _, msg_data = self.conn.fetch(num, "(RFC822)")
            raw_mail = msg_data[0][1]
            msg = email.message_from_bytes(raw_mail)
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            if subject.find('Transaction alert on Axis Bank Credit Card no') != 1:
                ref = str(msg).find('</span> <br><br>')
                print(ref)
                transaction_msg = str(str(msg)[ref + 82:ref + 82 + 185])
                transaction_msg = str(transaction_msg.replace("=\n", ''))
                match = re.search(r'Card no\.\s(\w+).*?INR\s(\d+)\s.*?at\s(.*?)\son', transaction_msg)
                print(transaction_msg)
                try:
                    if match:
                        receiver = validation(match.group(3), 'text')
                        sender = validation(match.group(1), 'text')
                        amount = validation(match.group(2), 'int')
                except:
                    receiver = ['E', 1]
                    sender = ['E', 1]
                    amount = [0, 1]

                anamoaly = receiver[1] + sender[1] + amount[1] if receiver[1] + sender[1] + amount[1] > 0 else 0

                self.all_transactions.append(
                    [self.user , 'sent', amount[0], receiver[0], sender[0], '', 'axis_credit', anamoaly])

    def get_categorised(self, transaction):
        try:
            AUTO_CAT = json.loads(open('auto_categorisation.json').read())
        except:
            AUTO_CAT = {"auto_category": {"Others": []}}
            print(f" auto_category json  not found in dir {os.getcwd()}")

        key_sentence = transaction[3].lower() + ' ' + transaction[5].lower()
        break_all = False
        for category in AUTO_CAT['auto_category']:
            if break_all: break
            if category == 'Others': transaction.insert(5, category)
            # special cases (debt) if message in " ['number'] " this format
            try:
                match_debt = re.search(r'\[(\d+)\]', transaction[5])
                if match_debt:
                    match_debt.group(1)
                    transaction.insert(5, 'DEBT-OUT')
                    break
            except:
                pass
            # normal search
            for keyword in AUTO_CAT['auto_category'][category]:
                match = re.search(r'\b' + re.escape(keyword.lower()) + r'\b', key_sentence, flags=re.IGNORECASE)
                if match:
                    transaction.insert(6, category)
                    break_all = True
                    break

    def datalog(self):
        count = 0
        for transaction in self.all_transactions:
            count = count + 1
            data_template = {
                "user": transaction[0],
                "date": self.pass_date,
                "transaction_type": transaction[1],
                "amount": transaction[2],
                "sender_bank": transaction[4],
                "receiver_bank": transaction[3],
                "message": transaction[6] if transaction[6] not in [' ', ''] else 'No Message',
                "category": transaction[5],
                "sub_category": transaction[6] if transaction[6] not in [' ', ''] else 'NC',
                "group": '-',
                "payment_method": transaction[7],
                "data_ts": str(self.ist_time)
                # "xtra"
            }
            # url = f'http://127.0.0.1:8000//dem/datalogdem/{count}/{transaction[0]}/{str(self.pass_date)}'
            url =  f'https://serveraura.pythonanywhere.com/dem/datalogdem/{count}/{transaction[0]}/{str(self.pass_date)}'
            if self.post:
                status = requests.post(url, json=data_template)
                print(status.json())
            else:
                print(data_template)
        return True


if __name__ == '__main__':

    data = json.loads(open('user_data.json').read())
    print(data['users'])
    for user in data['users']:
        GetSpendings(user, ['phone_pe', 'axis_credit'], date='2024-05-04' , post = True)
