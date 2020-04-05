import requests
# import requests_cache
import re
from lxml import etree


class JybLinks:
    base_url = 'http://www.jyb.cn'
    session = requests.session()

    def __init__(self, url=base_url):
        # requests_cache.install_cache()
        # requests_cache.clear()
        self.url = url

    def get_links(self, url="http://www.jyb.cn/rmtsy1240/zhxw/", rule="/html/body/div[2]/div/a"):
        response = self.session.get(url)
        response.encoding = "utf-8"
        response = response.text
        html_text = etree.HTML(response)
        links_dom = html_text.xpath(rule)
        links = []
        for link in links_dom:
            text = link.xpath("@href")[0]
            links.append(text)
        # print(response.text)
        # links = re.findall(r'href\=\"(http\:\/\/www\.jyb\.cn\/rmtlist[a-zA-Z0-9\.\/]+)\"', response.text)
        # links = re.findall(r'[\u4E00-\u9FA5]+', response.text)
        # print(links)
        # links = list(set(links))
        # for link in links:
        #     print(link)
        return links

    def get_chinese(self, url="http://www.jyb.cn/rmtsy1240/zhxw/", rule="/html/body/div[2]/div/a"):
        response = self.session.get(url)
        response.encoding = "utf-8"
        response = response.text
        html_text = etree.HTML(response)
        names_dom = html_text.xpath(rule)
        names = []
        for name in names_dom:
            text = name.xpath('text()')[0]
            names.append(text)
        return names


# this is a comment which has no sense

# this is the third comment
# this is the second commit.
