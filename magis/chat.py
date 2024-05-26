import json
from datetime import datetime

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage, FunctionCall
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
                        When you create an agent it should only be to enhance your capacity to give the best answer to user needs.
                        Once you created an agent you can use the agent to answer the user.
                        You can created multiple agent at once.
                        Choose the agents base on their expertise or to had context to your answer.
                        You can update an agent by recalling the create function with the same agent_name.
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
            tool_calls = response.choices[0].message.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    result = self.call_tool(tool_call.function)
                    self.messages.append(
                        ChatMessage(
                            role="tool", tool_call_id=tool_call.id, name=tool_call.function.name, content=result))
                response = self.client.chat(
                    model=self.model, messages=self.messages, tools=self.tools, tool_choice="auto")
                self.messages.append(response.choices[0].message)
            return self.messages[-1].content

        return "Unable to get request from chat, try again..."

    def call_tool(self, fn: FunctionCall):
        try:
            if fn.arguments:
                params = orjson.loads(fn.arguments)
                result = self.tool_by_name.get(fn.name)(**params)
                return result
        except Exception as e:
            return json.dumps({'error': str(e)})
