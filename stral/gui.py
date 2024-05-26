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


from nicegui import ui
from nicegui.events import ValueChangeEventArguments

class ExternalAPI:
    def __init__(self):
        self.swagger_url = ""
        self.api_key = ""

external_api = ExternalAPI()

def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__

def go():
    MISTRAL_API_KEY = "<Mistral API key>"
    MISTRAL_DOC_URL = "https://docs.mistral.ai/capabilities/function_calling/"
    SWAGGER_URL = external_api.swagger_url
    EXTERNAL_API_KEY = external_api.api_key

    def download_webpage(url):
        response = requests.get(url)
        return response.text

    api_key = MISTRAL_API_KEY
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
    ui.code(code)


ui.page_title('MagiStral Wizard')
ui.label('MagiStral Wizard').style('color: #6E93D6; font-size: 200%; font-weight: 300')
ui.label('This universal convert helps you to generate your Mistral AI function specification and implementation!')
ui.input('OpenAPI Specification (Swagger) YAML', on_change=show).style('width: 400px').bind_value(external_api, 'swagger_url')
ui.input('API key', on_change=show).style('width: 400px').bind_value(external_api, 'api_key')
ui.button('Generate Mistral AI function tool', on_click=go)
ui.run()


