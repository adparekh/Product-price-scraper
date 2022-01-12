from sys import setdlopenflags
from configuration import amazon_config as ac
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class GenerateReport:
    def __init__(self):
        pass


class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        self.currency = currency
        options = ac.get_web_driver_options()
        ac.set_ignore_certificate_error(options)
        ac.set_browser_as_incognito(options)
        self.driver = ac.get_chrome_web_driver(options)
        self.price_filter = "&rh=p_36%3A{}00-{}00".format(
            filters['min'], filters['max'])

    def run(self):
        print("Starting script...")
        print("Looking for {} products...".format(self.search_term))
        links = self.get_products_links()
        if not links:
            print("No links found. Stopping script.")
            return
        print("Received {} product links.".format(len(links)))
        print("Retrieving product info...")
        products = self.get_products_info(links)
        print("Received information for {} products".format(len(products)))
        self.driver.quit()
        return products

    def get_products_links(self):
        self.driver.get(self.base_url)
        searchBar = self.driver.find_element_by_id("twotabsearchtextbox")
        searchBar.send_keys(self.search_term)
        searchBar.send_keys(Keys.RETURN)
        time.sleep(2)
        self.driver.get("{}{}".format(
            self.driver.current_url, self.price_filter))
        time.sleep(2)
        results = self.driver.find_elements_by_css_selector(
            '.s-result-item.s-asin')
        if results == None:
            print("None")
        links = []
        # for result in results:
        #     print(result.text)
        try:
            links = [result.find_element_by_css_selector(
                ".a-link-normal.s-no-outline").get_attribute('href') for result in results]
        except Exception as excp:
            print("No products found.")
            print(excp)
# Some links are redirects. Those links are removed from the list.
        last_index = len(links) - 1
        while last_index >= 0:
            if links[last_index].find("picassoRedirect") != -1:
                del links[last_index]
            last_index -= 1
        return links

    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products

    def get_single_product_info(self, asin):
        print("Getting data for Product ID: {}".format(asin))
        product_short_url = self.shorten_url(asin)
        self.driver.get("{}".format(product_short_url))
        time.sleep(3)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_title(self):
        try:
            return self.driver.find_element_by_id("productTitle").text
        except Exception as excp:
            print("Could not retrieve the title of this product: {}".format(
                self.driver.current_url))
            print(excp)
            return None

    def clean_seller_name(self, byline_info):
        seller = ""
        if byline_info.find("Visit the ") != -1:
            seller = byline_info[10:byline_info.find(" Store")]
        elif byline_info.find("Brand: ") != -1:
            seller = byline_info[7:len(byline_info)]
        else:
            seller = byline_info
        return seller

    def get_seller(self):
        try:
            byline_info = self.driver.find_element_by_id("bylineInfo").text
            seller = self.clean_seller_name(byline_info)
            return seller
        except Exception as excp:
            print("Could not retrieve the byline info of this product: {}".format(
                self.driver.current_url))
            print(excp)
            return None

    def clean_price(self, price):
        price = price.split(self.currency)[1]
        if price.find("\n") != -1:
            price = price.split("\n")[0] + "." + price.split("\n")[1]
        return float(price)

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element_by_class_name(
                "apexPriceToPay").text
        except NoSuchElementException:
            try:
                price = self.driver.find_element_by_class_name(
                    "priceToPay").text
            except NoSuchElementException:
                try:
                    availability = self.driver.find_element_by_id(
                        "availability").text
                    if 'Not' not in availability:
                        price = self.driver.find_element_by_id("buyNew_noncbb")
                        price = price.find_element_by_css_selector(
                            ".offer-price").text
                except Exception as excp:
                    print("No stock available for the following product: {}".format(
                        self.driver.current_url))
            except Exception as excp:
                print("Cannot retrieve the price of this product: {}".format(
                    self.driver.current_url))
                print(excp)
        except Exception as excp:
            print("Cannot retrieve the price of this product: {}".format(
                self.driver.current_url))
            print(excp)
        if price:
            price = self.clean_price(price)
        return price

    def shorten_url(self, asin):
        return self.base_url + "dp/" + asin

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    def get_asin(self, link):
        return link[link.find('/dp/') + 4:link.find('/ref')]


if __name__ == '__main__':
    connect = ac.AmazonConfig()
    amazon = AmazonAPI(connect.name, connect.filters,
                       connect.base_URL, connect.currency)
    data = amazon.run()
    print(data)
