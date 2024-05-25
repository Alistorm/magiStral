import gradio

from magis.chat import generate_agent, MagisAgent


def agent_query(agent: MagisAgent):
    def query(message, history):
        return agent.invoke(message['text']).content

    return query


if __name__ == "__main__":
    agent = generate_agent()
    demo = gradio.ChatInterface(
        title="magiStral",
        fn=agent_query(agent),
        multimodal=True,
    )
    demo.launch()
