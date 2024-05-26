# -----------------------------------------------------------
# Mistral AI Paris Hackathon
# Date: 25/05/2024
# Author: Wilfred Doré
# -----------------------------------------------------------

import requests
import json

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from bs4 import BeautifulSoup

MISTRAL_API_KEY = "<insert Mistral AI client API key>"
MISTRAL_DOC_URL = "https://docs.mistral.ai/capabilities/function_calling/"

# TODO: replace/test with other Swagger YAML
SWAGGER_URL = "https://gist.githubusercontent.com/KPS250/7d1cfc06caefe82ba008eccf911bb3af/raw/37d1116e49b9c2c88cacd8453ffc61d710397efd/openweather_swagger.yaml"
EXTERNAL_API_KEY = "<insert OpenWeather Map or other API keys>"

def download_webpage(url):
    response = requests.get(url)
    return response.text

api_key = "<insert Mistral API key>"
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

prompt = f"""
Given your client documentation:
{ BeautifulSoup(download_webpage(MISTRAL_DOC_URL), features="lxml").get_text() }
and this external API OpenAPI YAML specification:
{ download_webpage(SWAGGER_URL) }
     
Generate a Python code to illustrate your Mistral AI function calling with this external API dynamically
- isolate API keys in constants, inject them in the code when relevant
- build the Mistral AI tools JSON specification
- find yourself a relevant prompt for testing the external API
- make sure to convert the function_result as string before providing it to the ChatMessage as content
- create a simple names_to_functions dict (function names as string and corresponding python functions)
- set Mistral chat temperature always to 0
- after receiving the first response from Mistral, do this: messages.append(response.choices[0].message)

The Mistral AI client API is {MISTRAL_API_KEY}
The external API key is {EXTERNAL_API_KEY}

Use mistral-large-latest model on Mistral client
You must give me a JSON response whose field "code" contains the whole code
"""
messages = [ChatMessage(role="user", content=prompt)]

chat_response = client.chat(
    model=model,
    temperature=0,
    response_format={"type": "json_object"},
    messages=messages,
)
code = json.loads(chat_response.choices[0].message.content)["code"]
code = code.replace("```python", "")
code = code.replace("```", "")
print(code)