# Description: A LangGraph Agent for answering the Hugging Face GAIA subset of 20 questions.
# Author: Thomas Purk
# Date: 2025-05-15
# Reference: https://langchain-ai.github.io/langgraph/agents/agents/

import os

from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from retreivers.woodoworking_retriever import woodworking_retriever_tool
from utils.utils import update_reporter

class woodworking_agent:
    def __init__(self):
        """TODO"""

        # Create the agent graph builder object
        self.graph_builder = StateGraph(MessagesState)

        # Tools Available to the LLM
        tools = [woodworking_retriever_tool]

        # Generate the chat interface, including the tools
        chat_model = init_chat_model(
            model=os.environ.get("CHAT_MODEL")
        )
        chat_model_with_tools = chat_model.bind_tools(
            tools=tools
        )

        # Define nodes: these do the work
        # chat_node to process the question
        def chat_node(state: MessagesState) -> dict:
            """ Forms an LLM response to the current MessageState message."""

            return {
                "messages": [chat_model_with_tools.invoke(state["messages"])],
            }
        
        # The first node is the chat
        self.graph_builder.add_node(
            node="chat_node", 
            action=chat_node
        )
        self.graph_builder.add_edge(
            start_key=START, # from node
            end_key="chat_node" # to node
        )

        # Tool node to select the tool requested from the last AI Message
        self.graph_builder.add_node(
            node="tools", 
            action=ToolNode(tools=tools)
        )
        self.graph_builder.add_conditional_edges(
            source="chat_node",
            # If the latest message (result) from chat_node is a tool call -> tools_condition routes to tools
            # If the latest message (result) from chat_node is a not a tool call -> tools_condition routes to END
            path=tools_condition,

        )
        # Return the flow to the chat_node to decide what to do next
        self.graph_builder.add_edge(
            start_key="tools", # from node
            end_key="chat_node" # to node
        )

        # Compile the Agent
        self.graph = self.graph_builder.compile()

    def __call__(self, content: str) -> str:
        """ Send request to the agent."""

        content_plus = f"""You are an AI Agent who uses tools to help provide accurate and concise answers. Based on the question, decided which tools, if any, to use that would help provide the best answer.

        Question:{content}""" 

        messages = [HumanMessage(content=content_plus)]

        response = "None"
        for chunk in self.graph.stream({"messages": messages}):
            for node, update in chunk.items():
               print( update_reporter(node,update))
               response = update["messages"][-1].content

        return response