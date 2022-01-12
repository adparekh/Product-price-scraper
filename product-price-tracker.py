from configuration import amazon as ac
from websites import amazon as az

import json
from datetime import datetime


class GenerateReport:
    def __init__(self, file_name, filters, base_link, currency, data):
        self.data = data
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        self.currency = currency
        report = {
            'title': self.file_name,
            'date': self.get_now(),
            'currency': self.currency,
            'price-filters': self.filters,
            'base_link': self.base_link,
            'products': self.get_sorted_data()
        }
        with open("reports/{}.json".format(self.file_name), 'w') as file:
            json.dump(report, file)

    def get_now(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def get_sorted_data(self):
        return sorted(self.data, key=lambda k: k['price'])


if __name__ == '__main__':
    connect = ac.AmazonConfig()
    amazon = az.AmazonAPI(connect.name, connect.filters,
                          connect.base_URL, connect.currency)
    data = amazon.run()
    report = GenerateReport(
        amazon.search_term, connect.filters, amazon.base_url, amazon.currency, data)
