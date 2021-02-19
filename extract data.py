import requests
from selectorlib import Extractor

e = Extractor.from_yaml_file('selector.yml')

# Download the page using requests
# r = requests.get('https://www.amazon.in/Infinity-Glide-500-Wireless-Headphones/dp/B07W5MYRF4/ref=sr_1_1_sspa?crid=384417BZYUPRB&dchild=1&keywords=headphone+wireless&qid=1613395289&smid=A14CZOWI0VEHLG&sprefix=headph%2Caps%2C-1&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExVkxNS1MwTkpGUVhWJmVuY3J5cHRlZElkPUEwNzc4NTExMTNTRkVZUTVHRzFTWCZlbmNyeXB0ZWRBZElkPUEwOTM4NDM1M0Y0VVYzUUhEUlhSOCZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=')
# r = requests.get('https://scrapeme.live/shop/')
r = requests.get('https://www.amazon.com/Sony-MDRZX110-BLK-Stereo-Headphones/dp/B00NJ2M33I/ref=sr_1_3?dchild=1&keywords=headphones&qid=1613717798&sr=8-3')
#
# # Pass the HTML of the page and create
# data = e.extract(r.text)
#
# # Print the data
# print(data)
