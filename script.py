# import requests
# from bs4 import BeautifulSoup as bs

# URL = 'https://www.amazon.ca/PS5-Horizon-Forbidden-West-Launch/dp/B09FBKM4GN/ref=sr_1_3?crid=3K935CMPPQWYE&keywords=ps5&qid=1641665254&sprefix=ps%2Caps%2C77&sr=8-3'
# # URL = input('Enter the amazon product link whose price is to be tracked: ')

# # header = input('Enter your user agent: ')
# headers = {
#     "User-Agent": 'Defined'}

# page = requests.get(URL, headers=headers)
# webpage = page.content
# soup = bs(webpage, 'html.parser')
# title = soup.find(id='productTitle')
# print(title)
