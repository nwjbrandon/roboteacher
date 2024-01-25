from roboteacher.utils import create_timestamp

SAMPLE_DATA = {
    "article_id": "nhk-news-web-easy",
    "url": "https://www.tofugu.com/japanese-learning-resources-database/nhk-news-web-easy",
    "title": "NHK Web Easy",
    "created_at": create_timestamp(),
    "article": """
For years, NHK News Web Easy has been one of the first stops for Japanese learners looking to improve their reading ability, and it’s no surprise why. With a wide selection of articles, and updates every day, NHK News Web Easy always manages to keep things fresh. As the name implies, articles come from NHK, the public national broadcasting corporation in Japan. Of course, these have been rewritten to be easy to understand for Japanese learners, making them accessible to pretty much anyone. Articles tend to be pretty short, and often include either a photo or video. Kanji has furigana above, should there be any words you’re unfamiliar with, though there’s a button to toggle this on and off if you want to challenge yourself. There’s also an audio option, though do note that these are machine generated rather than read by a person. Still, it can be nice to listen along as you read. \nFinally, articles have underlined words, which show a pop-up dictionary similar to Yomichan. These definitions are in Japanese, so there’s a bit of extra practice there! While reading the news might not be for everyone, with NHK News Web Easy’s variety of different articles, you’re sure to find a few that pique your interest. Especially for learners without much experience with reading practice in Japanese, you can’t do much better than NHK News Web Easy.
""".strip(),
    "translated_text": """
For years, NHK News Web Easy has been one of the first stops for Japanese learners looking to improve their reading ability, and it’s no surprise why. With a wide selection of articles, and updates every day, NHK News Web Easy always manages to keep things fresh. As the name implies, articles come from NHK, the public national broadcasting corporation in Japan. Of course, these have been rewritten to be easy to understand for Japanese learners, making them accessible to pretty much anyone. Articles tend to be pretty short, and often include either a photo or video. Kanji has furigana above, should there be any words you’re unfamiliar with, though there’s a button to toggle this on and off if you want to challenge yourself. There’s also an audio option, though do note that these are machine generated rather than read by a person. Still, it can be nice to listen along as you read. \nFinally, articles have underlined words, which show a pop-up dictionary similar to Yomichan. These definitions are in Japanese, so there’s a bit of extra practice there! While reading the news might not be for everyone, with NHK News Web Easy’s variety of different articles, you’re sure to find a few that pique your interest. Especially for learners without much experience with reading practice in Japanese, you can’t do much better than NHK News Web Easy.
""".strip(),
    "question": "What is NHK News Web Easy?",
    "choices": [
        {
            "choice": "A website for Japanese learners to improve their reading ability",
            "is_answer": True,
            "explanation": "",
        },
        {
            "choice": "A public national broadcasting corporation in Japan",
            "is_answer": False,
            "explanation": "",
        },
        {
            "choice": "A news website with articles about Japan",
            "is_answer": False,
            "explanation": "",
        },
        {
            "choice": "A website with audio books for Japanese learners",
            "is_answer": False,
            "explanation": "",
        },
    ],
    "audio_object_key": "audio/nhk-news-web-easy.mp3",
    "json_object_key": "audio/nhk-news-web-easy.json",
}
