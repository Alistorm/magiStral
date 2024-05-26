from multiprocessing import cpu_count, Pool

import gradio

from magis.chat import MagisAgent, agent_creator


def agent_query(agent: MagisAgent):
    def query(message, history):
        if message.get('files'):
            with Pool(processes=cpu_count()) as p:
                p.map()
        return agent.invoke(message['text'])

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
