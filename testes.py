import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=XPIKCR3UMMYHESHV'
r = requests.get(url)
data = r.json()

print(data)