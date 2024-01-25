import random

import pymongo
from bson.objectid import ObjectId

from roboteacher.utils import create_mongodb_connection


class ReadingComprehensionCollections:
    def __init__(
        self,
    ) -> None:
        self.db_conn = create_mongodb_connection()
        self.reading_comprehension = self.db_conn.ReadingComprehension
        self.max_documents = 100

    def insert(
        self,
        data: dict,
    ) -> dict:
        is_exist = self.exist(data)
        if is_exist:
            return {}

        self.reading_comprehension.insert_one(data)
        return {}

    def get(
        self,
    ) -> list:
        res: list = []
        items = self.reading_comprehension.find({}).sort(
            [
                ("created_at", pymongo.DESCENDING),
            ]
        )
        for item in items:
            del item["_id"]
            choices = item["choices"]
            random.shuffle(choices)
            item["choices"] = choices

            res.append(item)
        return res

    def exist(
        self,
        data: dict,
    ) -> bool:
        url = data["url"]
        if self.reading_comprehension.count_documents({"url": url}, limit=1) != 0:
            return True
        else:
            return False

    def delete(
        self,
    ):
        n_documents = self.reading_comprehension.count_documents({})
        if n_documents > self.max_documents:
            n_remove = n_documents - self.max_documents
            items = self.reading_comprehension.find({}).sort(
                [
                    ("created_at", pymongo.ASCENDING),
                ]
            )
            for i in range(n_remove):
                self.reading_comprehension.delete_one(
                    {
                        "_id": ObjectId(items[i]["_id"]),
                    }
                )
