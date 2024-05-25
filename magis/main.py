import gradio
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_groq import ChatGroq

from magis.chat import generate_agent, MagisAgent, agent_builder


def agent_query(agent: MagisAgent):
    def query(message, history):
        return agent.invoke(message['text']).content

    return query


if __name__ == "__main__":
    # agent = generate_agent()
    agent = agent_builder()
    demo = gradio.ChatInterface(
        title="magiStral",
        fn=agent_query(agent),
        multimodal=True,
    )
    demo.launch()
