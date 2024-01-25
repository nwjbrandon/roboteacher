import roboteacher.constants
from roboteacher.chatgpt import create_question_with_chatgpt

article = "Make yourself at ease with Japanese through this series of lessons. Tune in each week for a 10-minute episode or look for it online. Across 48 weeks, you'll learn the basic of the language and be ready for all sorts of conversations. Useful phrases are presented in skits that are fun and easy to remember. All sorts of travel information is included too, along with insights into culture and customs. Listen in and get talking."
language = "English"

print(create_question_with_chatgpt(article, language))
