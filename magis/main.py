import getpass
import os
from datetime import datetime

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_groq import ChatGroq

if __name__ == "__main__":
    chat = ChatGroq(temperature=0)
    messages = [
        SystemMessage(f"You are a helpful agent called Jarvis.Today is {datetime.now().isoformat()}."),
        AIMessage("Hello dude my name is Jarvis! How can I help ?")
    ]
    while True:
        messages.append(HumanMessage(input(messages[-1].content)))
        messages.append(chat.invoke(messages))
