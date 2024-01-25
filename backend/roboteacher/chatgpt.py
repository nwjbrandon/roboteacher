import json

from openai import OpenAI

from roboteacher.constants import LANGUAGES_ACRONYMS


def create_question_from_article_with_chatgpt(
    article: str,
    language: str,
) -> dict:
    language = LANGUAGES_ACRONYMS[language]

    user_prompt = f"""
    Create an exam question for reading comprehension with the article below.

    {article}


    Act as a language teacher who wants to set an exam to test reading comprehension skills.
    Task:
    A. Create 1 question only from the article in {language}.
    B. Create 4 options for the student to choose from.
    C. Create only 1 correct option out of the 4 options
    E. Give an explanation of why the option is correct/wrong
    F. Design the question to be challenging to answer
    """

    system_prompt = """
    Note:
    1. Give your output as only a RFC8259 compliant JSON response following this format without deviation.
    {
        "question": "the question to be answered",
        "choices": [
            {
                "choice": "the correct answer to the question",
                "is_answer": true,
                "explanation": "the explanation to why the answer is correct"
            },
            {
                "choice": "the wrong answer to the question",
                "is_answer": false,
                "explanation": "the explanation to why the answer is wrong"
            },
            {
                "choice": "the wrong answer to the question",
                "is_answer": false,
                "explanation": "the explanation to why the answer is wrong"
            },
            {
                "choice": "the wrong answer to the question",
                "is_answer": false,
                "explanation": "the explanation to why the answer is wrong"
            }
        ]
    }
    """

    client = OpenAI()

    completion = client.chat.completions.create(
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
    return output


def translate_article_with_chatgpt(
    article: str,
    from_language: str,
    to_language: str,
) -> dict:
    from_language = LANGUAGES_ACRONYMS[from_language]
    to_language = LANGUAGES_ACRONYMS[to_language]

    user_prompt = f"""
    Translate the article below.

    {article}


    Act as a {from_language} to {to_language} translator.
    Task:
    A. Translate the article from {from_language} to {to_language}.
    """

    system_prompt = """
    Note:
    1. Give your output of the translation in plain text without deviation.
    """

    client = OpenAI()

    completion = client.chat.completions.create(
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
    return output.strip()


def create_audio_voiceover_from_article_with_chatgpt(
    article: str,
    tmp_file: str,
) -> None:
    client = OpenAI()

    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=article,
    )
    response.stream_to_file(tmp_file)
