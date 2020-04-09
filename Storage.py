import pymongo


class MongoDB(object):
    def __init__(self):
        # self.client = pymongo.MongoClient("mongodb+srv://root:mongo123456...@cluster0-yahon.azure.mongodb.net/test")
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        print("成功")
        self.db = self.client['newsgroups']

    def insert(self, value):
        collection = self.db[value['类别']]
        collection.insert_one(value)
        print(value['标题'] + ":已插入")
