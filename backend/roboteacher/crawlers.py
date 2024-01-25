import time

import requests
from bs4 import BeautifulSoup


class NHK_Easy_News_Crawler:
    def __init__(
        self,
    ) -> None:
        self.root_url = "https://www3.nhk.or.jp/news/easy"
        self.recent_news_url = "https://www3.nhk.or.jp/news/easy/news-list.json"
        self.n_days = 3
        self.sleep_in_seconds = 0.2

    def get(
        self,
    ) -> list:
        articles = self.get_recent_articles()
        res = []
        for data in articles:
            ret, article = self.get_article(data)
            if not ret:
                continue

            data["article"] = article
            res.append(data)
        return res

    def get_recent_articles(
        self,
    ) -> list:
        response = requests.get(self.recent_news_url).json()
        response = response[0] if type(response) == list else response

        # Get recent articles
        dates = sorted(list(response.keys()))[-self.n_days :]
        articles = []
        for date in dates:
            articles.extend(response[date])

        res = []
        for article in articles:
            article_id = article["news_id"]
            article_title = article["title"]
            res.append(
                {
                    "article_id": article_id,
                    "url": f"{self.root_url}/{article_id}/{article_id}.html",
                    "title": self.sanitize_text(article_title),
                }
            )
        return res

    def get_article(
        self,
        data: dict,
    ) -> str:
        # Prevent 429 errors
        time.sleep(self.sleep_in_seconds)

        url = data["url"]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        body = soup.find_all("div", class_="article-main__body article-body")
        body = None if len(body) == 0 else body[0]
        if body is None:
            return False, None

        paragraphs = body.find_all("p")
        text = []
        for paragraph in paragraphs:
            text.append(paragraph.get_text())
        article = "\n".join(text)

        return True, self.sanitize_text(article)

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
