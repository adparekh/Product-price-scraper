from configuration import amazon_config as ac
import time


class GenerateReport:
    def __init__(self):
        pass


class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = ac.get_web_driver_options()
        ac.set_ignore_certificate_error(options)
        ac.set_browser_as_incognito(options)
        self.driver = ac.get_chrome_web_driver(options)
        self.price_filter = "rh=p_36%3A{}00-{}00".format(
            filters['min'], filters['max'])

    def run(self):
        print("Starting script...")
        print("Looking for {} products...".format(self.search_term))
        link = self.get_products_links()
        time.sleep(10)
        self.driver.quit()

    def get_products_links(self):
        self.driver.get(self.base_url)


if __name__ == '__main__':
    connect = ac.AmazonConfig()
    amazon = AmazonAPI(connect.name, connect.filters,
                       connect.base_URL, connect.currency)
    amazon.run()
