import os.path

import requests
from datetime import datetime, timedelta
import json


class label_data:
    def __init__(self, user, date, days):
        self.user = user
        self.url = 'https://serveraura.pythonanywhere.com//dem/api/get_labeled_data/'
        self.token_url = 'https://serveraura.pythonanywhere.com//dem/api/token/'
        self.token = ''
        self.end_date = str(date)
        self.days = days
        print(f'{user} - labelling from {days} to date {date}')
        self.save_label_data()

    def get_auth(self):
        token_data = {
            "username": 'sanjay',
            "password": "IamIronman"
        }
        req = requests.post(url=self.token_url, data=token_data)
        token = req.json()['access']

        auth = {
            'Authorization': 'Bearer ' + token
        }

        return auth

    def get_label_data(self):

        start_time = datetime.strptime(self.end_date, "%Y-%m-%d")-timedelta(days=self.days)
        start_time = str(start_time.strftime("%Y-%m-%d"))

        print(start_time , self.end_date)

        json_data = {
            "user": self.user,
            "start_date": start_time,
            "end_date": self.end_date
            # "start_date": start_time,
            # "end_date": self.end_date
        }

        req = requests.post(url=self.url, data=json_data, headers=self.get_auth())
        labels = {}
        print(req.json())
        for record in req.json():
            try:
                globals()[record['category']].append(record['receiver_bank'])
            except:
                globals()[record['category']] = []
                globals()[record['category']].append(record['receiver_bank'])
            labels[record['category']] = labels[record['category']] = globals()[record['category']]

        for key, values in labels.items(): labels[key] = list(set(values))
        return labels

    def save_label_data(self):

        file_name = self.user + '_dem_classifier.json'
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                json.dump(self.get_label_data(), file, indent=4)
        else:
            local_labeled_data = json.loads(open(file_name).read())
            new_labeled_data = self.get_label_data()

            for key in new_labeled_data:
                try:
                    local_labeled_data[key] = local_labeled_data[key] + new_labeled_data[key]
                except:
                    local_labeled_data[key] = new_labeled_data[key]

            for key, values in local_labeled_data.items(): local_labeled_data[key] = list(set(values))

            with open(file_name, 'w') as file:
                json.dump(local_labeled_data, file, indent=4)


if __name__ == '__main__':
    users = ['sanjay', 'avinash']
    for user in users:
        label_data(user, datetime.now().date(), 30)
