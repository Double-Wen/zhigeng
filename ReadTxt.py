import re

import requests
from bs4 import BeautifulSoup

from BloomFilter import BloomFilter
from Storage import MongoDB
from settings import category


class ReadTxt(object):
    def __init__(self, file):
        self.file = file
        self.mongodb = MongoDB()
        self.bf = BloomFilter()

    def read(self):
        news = []

        with open(self.file, 'r', encoding='utf-8-sig') as f:
            json = {
                '类别': '',
                'current_url': '',
                '标题': '',
                '文本链接': '',
                '概要': '',
                '作者': '',
                '来源': '',
                '发布时间': ''}
            current_url = ''
            while True:
                line = f.readline()
                if not line:
                    break
                if line[:-2] == '--------':
                    continue
                elif re.match("^current", line):
                    current_url = line[11:len(line) - 1]
                    json['类别'] = category.get(current_url[:30])
                    json['current_url'] = current_url
                    continue
                elif re.match('^http', line):
                    json['文本链接'] = line[:len(line) - 1]
                elif re.match('^作者', line):
                    author = f.readline()
                    if re.match('^[-]', author):
                        continue
                    author = author.replace('\t', '')
                    author = author.replace(' ', '')
                    json['作者'] = author[:len(author) - 1]
                elif re.match('^来源', line):
                    if not line[3:len(line) - 1]:
                        source = f.readline()
                        if re.match('^[-]', author):
                            continue
                        source = source.split(' ')[-1]
                        json['来源'] = source[:len(source) - 1]
                    else:
                        json['来源'] = line[3:len(line) - 1]
                elif re.match('^发布时间', line):
                    json['发布时间'] = line[5:len(line) - 1]
                    element = json.copy()
                    news.append(element)
                    json['标题'] = ''
                    json['概要'] = ''
                elif line[0] != '-':
                    if json['标题'] == '':
                        json['标题'] = line[:len(line) - 1]
                    else:
                        json['概要'] += line[:len(line) - 1]
                        json['概要'] += line[:len(line) - 1]
                        while True:
                            abstract = f.readline()
                            if re.match('^[-]', abstract):
                                break
                            abstract = abstract.replace('\x7f', '')
                            abstract = abstract.replace('\u3000', '')
                            json['概要'] += abstract[:len(abstract) - 1]

                if json.get('current_url') == '':
                    json['current_url'] = current_url
                    json['类别'] = category.get(current_url[:30])

            return news

    def get_text(self, values):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
        }
        for value in values:
            if self.bf.exists(value["标题"]):
                print(value['标题'] + "已存在")
                continue
            self.bf.insert(value['标题'])

            try:
                response = requests.get(
                    url=value['文本链接'],
                    headers=headers)
                if response.status_code == 200:
                    txt = '\t'
                    response.encoding = response.apparent_encoding
                    html = response.text
                    soup = BeautifulSoup(html, 'lxml')
                    soup = soup.select('.xl_text')[0]
                    soups = soup.find_all(name='p')
                    for soup in soups:
                        if soup.contents is not None:
                            children = soup.contents
                            for child in children:
                                if child.string is not None:
                                    txt += (child.string + ' ')
                            txt += "\n\t"
                        elif soup.string is not None:
                            txt += soup.string + '\n\t'
                    value['文本'] = txt
                    print(value['标题'] + ":查找成功")
            except Exception as e:
                print(value['文本链接'])

        return values

    def save(self, values):
        for value in values:
            self.mongodb.insert(value)


if __name__ == '__main__':
    reader = ReadTxt(r'D:\速盘解压\newprofile.txt')
    news = reader.read()
    news = reader.get_text(news)
    reader.save(news)
