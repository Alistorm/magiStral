import gradio

from magis.chat import LeMagisChat


def agent_query(agent: LeMagisChat):
    def query(message, history):
        return agent.invoke(message['text'])

    return query


def run():
    agent = LeMagisChat()
    demo = gradio.ChatInterface(
        title="magiStral",
        fn=agent_query(agent),
        multimodal=True,
    )
    demo.launch()


if __name__ == "__main__":
    run()
