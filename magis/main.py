from datetime import datetime

import gradio
from gradio.server_messages import BaseMessage
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_groq import ChatGroq

chat = ChatGroq(temperature=0)
messages: list[SystemMessage | AIMessage | HumanMessage] = [
    SystemMessage(f"You are a helpful agent called Jarvis.Today is {datetime.now().isoformat()}."),
    AIMessage("Hello dude my name is Jarvis! How can I help ?")
]


def query(message, history):
    messages.append(HumanMessage(message['text']))
    response = chat.invoke(messages)
    if response.type == 'ai':
        messages.append(AIMessage(response.content))
    return messages[-1].content


if __name__ == "__main__":
    demo = gradio.ChatInterface(
        fn=query,
        title="magiStral",
        multimodal=True,
    )
    demo.launch()
