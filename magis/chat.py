from datetime import datetime

from langchain_core.messages import SystemMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI


class MagisAgent:
    def __init__(self, groq=False, messages=None):
        self.chat = ChatGroq(temperature=0) if groq else ChatMistralAI(temperature=0)
        self.messages = messages if messages else []

    def invoke(self, message):
        self.messages.append(message)
        self.messages.append(self.chat.invoke(self.messages))
        return self.messages[-1]


def generate_agent() -> MagisAgent:
    messages = [
        SystemMessage(f"You are a helpful agent called Jarvis.Today is {datetime.now().isoformat()}."),
        AIMessage("Hello dude my name is Jarvis! How can I help ?")
    ]
    return MagisAgent(messages=messages)
