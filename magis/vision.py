import requests

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}


def generate_vision(filename, question):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data={
        'image': data.,
        'question': question
    })
    return response.json()