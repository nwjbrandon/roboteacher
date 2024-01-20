import json
import traceback

import boto3
from openai import OpenAI

from roboteacher.constants import S3_BUCKET_AUDIO


class Prompt:
    def __init__(
        self,
    ) -> None:
        self.client = OpenAI()

    def generate(
        self,
        article: dict,
    ) -> tuple:
        content = article["content"]

        user_prompt = f"""
        Create exam question for reading comprehension with the article below.

        {content}
        """

        system_prompt = """
        Act as a language teacher who wants to set an exam to test her students' reading comprehension skills.
        Task:
        A. Create a question from the article in Japanese.
        B. Create 4 options for the student to choose from.
        C. Give the correct answer from the 4 options.

        Note:
        1. Give only 1 correct option.
        2. Give your output as \{"question": "Question", "options": [{"option": "Option 1", "isAnswer": true }, {"option": "Option 2", "isAnswer": false }, {"option": "Option 3", "isAnswer": false }, {"option": "Option 4", "isAnswer": false }]\}
        """
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
            )

            output = completion.choices[0].message.content
            output = json.loads(output)
            return True, output
        except:
            print("output:", output)
            print(traceback.format_exc())
            return False, None

    def translate(
        self,
        article: dict,
    ) -> tuple:
        content = article["content"]

        user_prompt = f"""
        Translate the article below into English

        {content}
        """

        system_prompt = """
        Act as a Japanese to English translator.
        Task:
        A. Translate the article from Japanese to English.
        """
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
            )

            output = completion.choices[0].message.content
            return True, output
        except:
            print("output:", output)
            print(traceback.format_exc())
            return False, None

    def voiceover(
        self,
        article: dict,
    ) -> bool:
        article_id = article["articleId"]
        tmp_audio_fname = f"/tmp/{article_id}.mp3"
        content = article["content"]

        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=content,
            )
            response.stream_to_file(tmp_audio_fname)
            return True
        except:
            print(traceback.format_exc())
            return False

    def save(
        self,
        article: dict,
    ) -> bool:
        ret = self.save_article_to_tmp(article)
        if not ret:
            return False

        try:
            article_id = article["articleId"]
            self.save_audio_in_s3(article_id)
            self.save_json_in_s3(article_id)
            return True
        except:
            print(traceback.format_exc())
            return False

    def save_article_to_tmp(
        self,
        article: dict,
    ) -> bool:
        try:
            article_id = article["articleId"]
            tmp_file = f"/tmp/{article_id}.json"
            with open(tmp_file, "w") as f:
                json.dump(article, f, indent=2)
            return True
        except:
            return False

    def save_audio_in_s3(
        self,
        article_id: str,
    ) -> str:
        tmp_audio_fname = f"/tmp/{article_id}.mp3"
        s3_audio_object_key = f"audio/{article_id}.mp3"

        s3 = boto3.resource("s3")
        s3.Bucket(S3_BUCKET_AUDIO).upload_file(tmp_audio_fname, s3_audio_object_key)
        return

    def save_json_in_s3(
        self,
        article_id: str,
    ) -> str:
        tmp_json_fname = f"/tmp/{article_id}.json"
        s3_json_object_key = f"audio/{article_id}.json"

        s3 = boto3.resource("s3")
        s3.Bucket(S3_BUCKET_AUDIO).upload_file(tmp_json_fname, s3_json_object_key)
        return
