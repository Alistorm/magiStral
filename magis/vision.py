import os

import requests


def generate_vision(filename: str) -> str:
    with open(filename, "rb") as f:
        data = f.read()
    with requests.post(
            "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large",
            headers={"Authorization": f"Bearer {os.getenv('HUG_FACE_TOKEN')}"},
            data=data) as r:
        return r.json()[0]['generated_text'].replace('araffe', '').strip()


if __name__ == "__main__":
    print(generate_vision('ressources/sample.png'))
