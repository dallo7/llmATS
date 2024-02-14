import time
import requests
import formatString


def flant5xxl(resumeText):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    time.sleep(5)

    txt = formatString.removeFormat(resumeText)

    output = query({
        "inputs": f"Assume you are a recruiter, Score or Rate the resume shared Based on each experience, Python Experience , Deep learning Experience, AWS Experience : Rate this Applicants resume {txt}"
    })

    return output


def facebookBL(text):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({"inputs": text})

    output = output[0]["summary_text"]

    return output
