from selenium import webdriver


class AmazonConfig:
    def __init__(self):
        self.directory = 'reports'
        self.name = input("Enter the product to be searched: ")
        self.currency = '$'
        self.min_price = input("Enter the minimum price range: ")
        self.max_price = input("Enter the maximum price range: ")
        self.filters = {
            'min': self.min_price,
            'max': self.max_price
        }
        self.base_URL = 'https://www.amazon.ca/'

    def __str__(self):
        return "Name: {}\nCurrency: {}\nMinimum Price: {}\nMaximum Price:{}\nbase URL: {}".format(self.name, self.currency, self.min_price, self.max_price, self.base_URL)


def get_chrome_web_driver(options):
    return webdriver.Chrome('./chromedriver', chrome_options=options)


def get_web_driver_options():
    return webdriver.ChromeOptions()


def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')


def set_browser_as_incognito(options):
    options.add_argument('--incognito')
