import start
import requests
import pymysql

links = start.JybLinks().get_links()
print(links)
names = start.JybLinks().get_chinese()
print(names)
for i, j in zip(links[2:-1], names[2: -1]):
    print(i, j)
session = requests.session()
# for link in links[0:1]:
#     print(link)
#     response = session.get(link)
#     response.encoding = 'utf-8'
#     print(response.text)
