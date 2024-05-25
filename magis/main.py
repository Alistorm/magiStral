import json

import gradio as gr
from langchain_core.messages import SystemMessage, HumanMessage

from magis.chat import MagisAgent, generate_magis_agent


def agent_query(agent: MagisAgent):
    def query(message, history):
        response = agent.invoke(message['text']).content
        if '{' in response and '}' in response:
            print(response)
            start, end = response.index('{'), response.index('}') + 1
            agent.messages = [SystemMessage(json.loads(response[start:end])['systeme'])]
            response = agent.invoke(HumanMessage(message['text'])).content
        return response

    return query


if __name__ == "__main__":
    agent = generate_magis_agent()
    # agent = agent_builder()
    agents = []

    # Create the Gradio interface
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=1):
                agents = gr.CheckboxGroup(label="Agents", choices=agents)
            with gr.Column(scale=10):
                gr.ChatInterface(
                    title="magiStral",
                    fn=agent_query(agent),
                    multimodal=True,
                )
    # Launch the Gradio interface
    demo.launch()
