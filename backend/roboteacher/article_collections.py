import random

import pymongo
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from roboteacher.constants import DB_HOSTNAME, DB_NAME, DB_PASSWORD, DB_USERNAME


class ArticleCollections:
    def __init__(
        self,
    ) -> None:
        self.db_uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/?retryWrites=true&w=majority"
        self.client = MongoClient(self.db_uri, server_api=ServerApi("1"))
        self.db_name = self.client[DB_NAME]
        self.articles = self.db_name.Articles
        self.max_documents = 300

    def insert(
        self,
        data: dict,
    ) -> dict:
        is_exist = self.exist(data)
        if is_exist:
            return {}

        self.articles.insert_one(data)
        return {}

    def get(
        self,
    ) -> list:
        res: list = []
        items = self.articles.find({}).sort(
            [
                ("createdAt", pymongo.DESCENDING),
            ]
        )
        for item in items:
            del item["_id"]
            options = item["options"]
            random.shuffle(options)
            item["options"] = options

            res.append(item)
        return res

    def exist(
        self,
        data: dict,
    ) -> bool:
        url = data["url"]
        if self.articles.count_documents({"url": url}, limit=1) != 0:
            return True
        else:
            return False

    def delete(
        self,
    ):
        n_documents = self.articles.count_documents({})
        if n_documents > self.max_documents:
            n_remove = n_documents - self.max_documents
            items = self.articles.find({}).sort(
                [
                    ("createdAt", pymongo.ASCENDING),
                ]
            )
            for i in range(n_remove):
                self.articles.delete_one(
                    {
                        "_id": ObjectId(items[i]["_id"]),
                    }
                )
