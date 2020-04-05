import requests
# import requests_cache
import re


class JybLinks:
    url = 'http://www.jyb.cn'
    session = requests.session()

    def __init__(self, url):
        # requests_cache.install_cache()
        # requests_cache.clear()
        self.url = url

    def get_links(self):
        url = self.url
        session = requests.session()
        response = session.get(url)
        # print(response.text)
        links = re.findall(r'href\=\"(http\:\/\/www\.jyb\.cn\/rmtlist[a-zA-Z0-9\.\/]+)\"', response.text)
        # print(links)
        links = list(set(links))
        # for link in links:
        #     print(link)
        return links

# this is a comment which has no sense

# this is the third comment
# this is the second commit.
