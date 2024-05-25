import gradio

from magis.chat import MagisAgent, agent_creator


def agent_query(agent: MagisAgent):
    def query(message, history):
        return agent.invoke(message['text']).content

    return query


if __name__ == "__main__":
    # agent = generate_agent()
    agent = agent_creator()
    demo = gradio.ChatInterface(
        title="magiStral",
        fn=agent_query(agent),
        multimodal=True,
    )
    demo.launch()
