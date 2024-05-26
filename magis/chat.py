from datetime import datetime

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from orjson import orjson

from magis.tools.main_tools import agent_creator_tool, agent_caller_tool


class LeMagisChat:
    def __init__(self, agents: dict = None, model="mistral-large-latest"):
        self.agents = agents if agents else {}
        self.client = MistralClient()
        self.model = model
        self.messages = [
            ChatMessage(
                role='system',
                content=f"""Today is {datetime.now()}.
                        You are a Magis helpful assistant with the ability to create and use expert agents to answer user needs.
                        When you create an agent it is to enhance your capacity to answer best to the user needs.
                        Once you created an agent you can use the agent to answer the user.
                        Choose the agent if you think he has the expertise or to had context to your answer.
                        """)
        ]
        self.tool_by_name = {}
        self.tools = []
        for tool in [agent_creator_tool, agent_caller_tool]:
            name, description, fn = tool(self)
            self.tool_by_name[name] = fn
            self.tools.append(description)

    def invoke(self, message: str) -> str:
        if message:
            self.messages.append(ChatMessage(role="user", content=message))
            response = self.client.chat(model=self.model, messages=self.messages, tools=self.tools, tool_choice="auto")
            self.messages.append(response.choices[0].message)
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    name = tool_call.function.name
                    params = orjson.loads(tool_call.function.arguments)
                    result = self.tool_by_name[name](**params)
                    self.messages.append(ChatMessage(role="tool", name=name, content=result, tool_call_id=tool_call.id))
                response = self.client.chat(model=self.model, messages=self.messages, tools=self.tools,
                                            tool_choice="auto")
                self.messages.append(response.choices[0].message)
            # Extract and return response content
            return response.choices[0].message.content

        return "Unable to get request from chat, try again..."
