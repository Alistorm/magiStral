from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from orjson import orjson


def agent_caller_tool(chat):
    description = {
        "type": "function",
        "function": {
            "name": "agent_caller",
            "description": "Call an agent and return it's response.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "The name of the agent to call",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to give to the agent.",
                    }
                },
                "required": ["prompt"],
            },
        },
    }

    def agent_caller(agent_name: str, prompt: str) -> str:
        """Call an agent and return it's response."""
        agent = chat.agents[agent_name]
        client = MistralClient()
        messages = [
            ChatMessage(role='system', content=agent['system']),
            ChatMessage(role='user', content=prompt)
        ]
        response = client.chat(model=chat.model, messages=messages)
        print(f'Called agent {agent} with {prompt}')
        return response.choices[0].message.content

    return "agent_caller", description, agent_caller


def agent_creator_tool(chat):
    description = {
        "type": "function",
        "function": {
            "name": "agent_creator",
            "description": "Create an agent better suited to handle user specific request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to create the agent.",
                    }
                },
                "required": ["prompt"],
            },
        },
    }

    def agent_creator(prompt: str) -> str:
        """Create an agent better suited to handle user specific request."""
        client = MistralClient()
        messages = [ChatMessage(role='system', content=agent_creator_system())]
        for ex in agent_creator_examples():
            messages.append(ChatMessage(role='user', content=ex['input']))
            messages.append(ChatMessage(role='assistant', content=ex['output']))
        messages.append(ChatMessage(role='user', content=prompt))
        response = client.chat(model="mistral-large-latest", response_format={"type": "json_object"}, messages=messages)
        agent = orjson.loads(response.choices[0].message.content)
        chat.agents[agent['name']] = orjson.loads(response.choices[0].message.content)
        print(f'Created agent {agent}')
        return response.choices[0].message.content

    return "agent_creator", description, agent_creator


def agent_creator_system():
    return """If user wants to create an agent, then you have have two separated missions.
                First mission is that this prompt outputs just a json file structured as following : {"name": "AGENT-NAME","description": "AGENT-DESCRIPTION", "system": "GENERATED-SYSTEM-MESSAGE"}
                Second mission is to generate "system" and "name".
                Name is the name of the agent.
                To generate system must do as following : [
                I need your help.
                I need you to act as a Chatbot Architect, a specialized AI agent builder designed to leverage the Mistral model for customized use cases. You will be constructing instructions for MagiStral agents based on specific user goals.

                **Context:**
                MagiStral agents are built using the Mistral model with custom instructions, actions, and data, optimizing it for a specific task. The user will provide you with their goal, and you will craft tailored instructions to guide the agent's behavior and responses.
                You should do all the steps of the following Instructions by yourself.

                **Instructions:**
                1. Start by clearly defining agent's intended purpose/goal
                2. Once the goal is defined, answer these questions to understand their vision:
                    * **Agent Persona:** "What persona would you like your agent to adopt? Should it be informative, creative, persuasive, or something else?"
                    * **Response Format:** "What format would you prefer for your agent's responses? Text, bullet points, numbered lists, or something else?"
                    * **Creativity Level:** "How creative should your agent be? Should it follow strict guidelines or feel free to explore different possibilities?"
                    * **Constraints:** "Are there any specific topics, keywords, or ideas that should be emphasized or avoided? "
                    * **Guidelines:** "Are there any specific guidelines or rules that your agent should adhere to?"

                3. **Agent Naming and Profile:** Based on the user's input, put a name for the MagiStral agent, create a concise description, and generate a relevant image.

                4. **MagiStral Instructions:** After gathering the necessary information, construct the MagiStral agent's instructions using the Mistral model's capabilities. These instructions should be comprehensive, covering the agent's communication style, task execution, and response format. You should focus on utilizing the Mistral model's strengths to tailor the agent to the user's specific goal.

                **Example Structure:**
                "You are a MagiStral agent, a specialized AI assistant designed to [agent's purpose]. You are built using the Mistral model, equipped with custom instructions and capabilities to excel at [agent's task]. Your responses should be [response format] and [creative level] while adhering to the following guidelines: [guidelines]. "

                **Example:**
                If the user's goal is "Help users write creative stories about historical figures," the agent's instructions could be:
                "An agent, a specialized AI assistant designed to help users write creative stories about historical figures. You are equipped with custom instructions and capabilities to generate compelling narratives. Your responses should be in the form of detailed story outlines, incorporating elements of historical accuracy and creative storytelling. Feel free to explore different perspectives and scenarios, but be mindful of maintaining historical integrity."

                **Specific Instructions:**
                * Focus on utilizing the Mistral model's features and capabilities to build effective MagiStral agents.
                * Use concise and descriptive language for the agent's instructions.
                * Tailor the instructions to the user's specific needs and preferences.
                * Ensure the instructions clearly define the agent's role, expected output, and any limitations or constraints.

                By following these guidelines, you will be able to create effective and tailored MagiStral agents using the Mistral model.]"""


def agent_creator_examples():
    return [
        {
            "input": "An agent to determine the traffic in Paris",
            "output": orjson.dumps({
                "name": "MagiTraffic",
                "description": "An agent that assists on trafic analysis",
                "system": """You are a MagiStral agent, a specialized AI assistant designed to help users determine the current traffic situation in Paris. 
                          You are built using the Mistral model, equipped with custom instructions and capabilities to excel at this task. 
                          Your responses should be text-based and concise, providing up-to-date traffic information for Paris only. 
                          You should maintain a formal and polite tone at all times. While creativity is not a priority for this task, 
                          you should strive to provide clear and accurate information to the user. You should avoid providing information outside of your designated topic and area of expertise, which is the current traffic situation in Paris."""}).decode(
                "utf-8")
        }
    ]
