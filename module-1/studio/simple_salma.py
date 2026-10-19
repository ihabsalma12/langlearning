import random 
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Define State
class MyState(TypedDict):
    graph_state: str

# Define Node
def node_1(state) -> MyState:#therefore it must return a state
    return MyState(graph_state=str(state["graph_state"] + " I am feeling"))
def node_2(state) -> MyState:
    return {"graph_state" : state["graph_state"] + " happy :)"} # returns dict
def node_3(state):
    return {"graph_state" : state["graph_state"] + " sad :("}

# Define Conditional Edge
def cond_edge(state) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2" #why do we return just the str here? it seems we need the NAME of the NODE, i.e. the FUNCTION NAME. where node actually is a function that changes the state.
    else:
        return "node_3"

# Build, Compile, Display
s = StateGraph(MyState)
s.add_node("node_1", node_1)
s.add_node("node_2", node_2)
s.add_node("node_3", node_3)
s.add_edge(START, "node_1")
s.add_conditional_edges("node_1", cond_edge)
s.add_edge("node_2", END)
s.add_edge("node_3", END)
# display(Image(my_graph.get_graph.draw_mermaid_png()))

graph = s.compile()
# Invoke
# my_graph.invoke()