import random
from typing import Annotated, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, MessagesState, StateGraph, add_messages
from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition

# Tools
def rand_choice_selector(choices: list[str]) -> str:
    """Selects one item randomly, given a list of items"""
    return random.choice(choices)

def rand_number_generator(min: int, max: int) -> int:
    """Returns a random number between a given range"""
    return random.randint(min, max)

# State
class MyState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages] # We need to append the messages between every node, 
    # or every new message rewrites the old message. This causes the llm to freak out when the message is empty and only has a tool call
    # response.

class MyMessagesState(MessagesState):
    pass # no need to put annotated here, since no reduction will happen, since no branching simultaneously... will implement in next one.




# LLM
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
my_tools = [rand_choice_selector, rand_number_generator]
llm = llm.bind_tools(my_tools)

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with writing performing arithmetic on a set of inputs.")

# Nodes
def llm_node(state: MyState) -> MyState:
    return {"messages": [  llm.invoke(state["messages"])  ]} # .invoke takes LanguageModelInput and returns AIMessage



# StateGraph
s = StateGraph(MyState)
s.add_node("llm_node", llm_node)
s.add_node("tools", ToolNode(my_tools))
s.add_edge(START, "llm_node")
s.add_conditional_edges("llm_node", tools_condition) # imported function that routes to tools OR END
s.add_edge("tools", "llm_node")

s.compile()