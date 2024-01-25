import json
import traceback

import boto3
from openai import OpenAI

from roboteacher.chatgpt import (
    create_audio_voiceover_from_article_with_chatgpt,
    create_question_from_article_with_chatgpt,
    translate_article_with_chatgpt
)
from roboteacher.constants import S3_BUCKET_AUDIO


class ReadingComprehension:
    def __init__(
        self,
    ) -> None:
        self.client = OpenAI()

    def generate_question(
        self,
        data: dict,
        language: str,
    ) -> tuple:
        article = data["article"]
        try:
            return True, create_question_from_article_with_chatgpt(
                article,
                language,
            )
        except:
            print(traceback.format_exc())
            return False, None

    def translate_passage(
        self,
        data: dict,
        from_language: str,
        to_language: str,
    ) -> tuple:
        article = data["article"]
        try:
            return True, translate_article_with_chatgpt(
                article,
                from_language,
                to_language,
            )
        except:
            print(traceback.format_exc())
            return False, None

    def generate_audio(
        self,
        data: dict,
    ) -> bool:
        tmp_file = f"/tmp/{data['article_id']}.mp3"
        article = data["article"]

        try:
            create_audio_voiceover_from_article_with_chatgpt(
                article,
                tmp_file,
            )
            return True
        except:
            print(traceback.format_exc())
            return False

    def save_data_to_s3(
        self,
        data: dict,
    ) -> bool:
        ret = self.save_data_to_tmp(data)
        if not ret:
            return False

        article_id = data["article_id"]
        try:
            self.upload_audio_file_to_s3(article_id)
            self.upload_json_file_to_s3(article_id)
            return True
        except:
            print(traceback.format_exc())
            return False

    def save_data_to_tmp(
        self,
        article: dict,
    ) -> bool:
        try:
            article_id = article["article_id"]
            tmp_file = f"/tmp/{article_id}.json"
            with open(tmp_file, "w") as f:
                json.dump(article, f, indent=2)
            return True
        except:
            return False

    def upload_audio_file_to_s3(
        self,
        article_id: str,
    ) -> str:
        tmp_file = f"/tmp/{article_id}.mp3"
        object_key = f"audio/{article_id}.mp3"

        s3 = boto3.resource("s3")
        s3.Bucket(S3_BUCKET_AUDIO).upload_file(tmp_file, object_key)
        return

    def upload_json_file_to_s3(
        self,
        article_id: str,
    ) -> str:
        tmp_file = f"/tmp/{article_id}.json"
        object_key = f"audio/{article_id}.json"

        s3 = boto3.resource("s3")
        s3.Bucket(S3_BUCKET_AUDIO).upload_file(tmp_file, object_key)
        return
