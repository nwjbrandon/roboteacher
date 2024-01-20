from roboteacher.article_collections import ArticleCollections
from roboteacher.constants import S3_BUCKET_AUDIO
from roboteacher.prompt import Prompt
from roboteacher.sample import SAMPLE_DATA
from roboteacher.scraper import Scrapper
from roboteacher.utils import create_timestamp


def scrap_data():
    chatgpt = Prompt()
    scrapper = Scrapper()
    article_collections = ArticleCollections()

    articles = scrapper.get()
    print("n_articles:", len(articles))

    for idx, article in enumerate(articles):
        article_id = article["articleId"]
        url = article["url"]
        print(idx, article_id, url)

        is_exists = article_collections.exist(article)
        if is_exists:
            continue

        ret, question = chatgpt.generate(article)
        if not ret:
            continue

        ret, translated = chatgpt.translate(article)
        if not ret:
            continue

        ret = chatgpt.voiceover(article)
        if not ret:
            continue

        article = {
            **article,
            **question,
            "translated": translated,
            "audioObjectKey": f"audio/{article_id}.mp3",
            "jsonObjectKey": f"audio/{article_id}.json",
            "createdAt": create_timestamp(),
        }

        ret = chatgpt.save(article)
        if not ret:
            continue

        article_collections.insert(article)
        break

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
    article_collections = ArticleCollections()
    articles = article_collections.get()
    res = []
    for article in articles:
        audio_filename = article["audioObjectKey"]
        article["audioObjectKey"] = f"https://{S3_BUCKET_AUDIO}.s3.ap-southeast-1.amazonaws.com/{audio_filename}"
        res.append(article)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": {
            "message": "Success",
            "articles": res,
        },
    }


def seed_data():
    article_collections = ArticleCollections()
    is_exists = article_collections.exist(SAMPLE_DATA)
    if not is_exists:
        article_collections.insert(SAMPLE_DATA)


def delete_data():
    article_collections = ArticleCollections()
    article_collections.delete()
