import time

import requests
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(
        self,
    ) -> None:
        self.recent_articles_url = "https://www3.nhk.or.jp/news/easy/news-list.json"
        self.root_url = "https://www3.nhk.or.jp/news/easy"

    def get(
        self,
    ) -> list:
        articles = self.get_recent_article_urls()
        res = []
        for article in articles:
            ret, content = self.get_article_content(article)
            if not ret:
                continue

            article["content"] = content
            res.append(article)
        return res

    def get_recent_article_urls(
        self,
    ) -> list:
        response = requests.get(self.recent_articles_url).json()
        response = response[0] if type(response) == list else response

        # Get earliest articles
        dates = sorted(list(response.keys()))[-3:]
        articles = []
        for date in dates:
            articles.extend(response[date])

        res = []
        for article in articles:
            article_id = article["news_id"]
            article_title = article["title"]
            res.append(
                {
                    "articleId": article_id,
                    "url": f"{self.root_url}/{article_id}/{article_id}.html",
                    "title": self.sanitize_text(article_title),
                }
            )
        return res

    def get_article_content(
        self,
        article: dict,
    ) -> str:
        # Prevent 429 errors
        time.sleep(0.2)

        article_url = article["url"]
        page = requests.get(article_url)
        soup = BeautifulSoup(page.content, "html.parser")

        article = soup.find_all("div", class_="article-main__body article-body")
        article = None if len(article) == 0 else article[0]
        if article is None:
            return False, None

        paragraphs = article.find_all("p")
        text = []
        for paragraph in paragraphs:
            text.append(paragraph.get_text())
        content = "\n".join(text)

        return True, self.sanitize_text(content)

    def sanitize_text(
        self,
        text: str,
    ) -> str:
        text = text.strip()
        text = text.replace("\u3000", " ")
        paragraphs = []
        for paragraph in text.split("\n"):
            paragraph = paragraph.strip()
            if paragraph == "":
                continue
            paragraphs.append(paragraph)
        paragraphs = "\n".join(paragraphs)
        return paragraphs
