
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
