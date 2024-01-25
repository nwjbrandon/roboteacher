import json

import humps

from roboteacher.collections import ReadingComprehensionCollections
from roboteacher.constants import S3_BUCKET_AUDIO
from roboteacher.crawlers import NHK_Easy_News_Crawler
from roboteacher.reading_comprehension import ReadingComprehension
from roboteacher.sample import SAMPLE_DATA
from roboteacher.utils import create_timestamp


def scrap_data():
    chatgpt = ReadingComprehension()
    scrapper = NHK_Easy_News_Crawler()
    reading_comprehension_collections = ReadingComprehensionCollections()

    articles = scrapper.get()
    print("n_articles:", len(articles))

    for idx, data in enumerate(articles):
        article_id = data["article_id"]
        print(idx, article_id, data["url"])

        is_exists = reading_comprehension_collections.exist(data)
        if is_exists:
            continue

        ret, question = chatgpt.generate_question(data, "jp")
        if not ret:
            continue

        ret, translated_text = chatgpt.translate_passage(data, "jp", "en")
        if not ret:
            continue

        ret = chatgpt.generate_audio(data)
        if not ret:
            continue

        output = {
            **data,
            **question,
            "translated_text": translated_text,
            "audio_object_key": f"audio/{article_id}.mp3",
            "json_object_key": f"audio/{article_id}.json",
            "created_at": create_timestamp(),
        }

        ret = chatgpt.save_data_to_s3(output)
        if not ret:
            continue

        reading_comprehension_collections.insert(output)

    delete_data()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": {
            "message": "Success",
        },
    }


def fetch_data():
    reading_comprehension_collections = ReadingComprehensionCollections()
    articles = reading_comprehension_collections.get()
    res = []
    for article in articles:
        audio_filename = article["audio_object_key"]
        article["audio_object_key"] = f"https://{S3_BUCKET_AUDIO}.s3.ap-southeast-1.amazonaws.com/{audio_filename}"
        res.append(article)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": {
            "message": "Success",
            "articles": humps.camelize(res),
        },
    }


def seed_data():
    article_collections = ReadingComprehensionCollections()
    is_exists = article_collections.exist(SAMPLE_DATA)
    if not is_exists:
        article_collections.insert(SAMPLE_DATA)


def delete_data():
    article_collections = ReadingComprehensionCollections()
    article_collections.delete()


def test():
    print(json.dumps(scrap_data(), indent=2))
    seed_data()
    print(json.dumps(fetch_data(), indent=2, ensure_ascii=False))
    delete_data()
