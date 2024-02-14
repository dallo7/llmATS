import time
import requests


def removeFormat(text):

    sentences = text.split('.')

    sentences = [sentence.strip() for sentence in sentences]

    paragraph = ' '.join(sentences)

    paragraph = paragraph.replace("•", "").replace("-", "")

    paragraph = paragraph.replace('\n', ' ').rstrip().strip().replace("   ", "").replace("    ", "").replace("  ", "")

    return paragraph


def formatLLMOutput(text):
    text_with_commas = text.replace("years", "years,")

    text_list = text_with_commas.split(',')

    text_list = [item.strip() for item in text_list]

    return text_list


def flanUL2(av):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-ul2"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    time.sleep(5)

    output = query({"inputs": f"For example The sum of digital experience 7 years, Cake experience 2 years, drug experience 5 years is 7 years + 2 years + 5 years = 14 years.  What is the sum of the following experience. :{av}"})

    return output
