Steps I follow:

1. watch the videos
2. look at the notebook and predict before running
3. running
4. after the lesson try to write it again by yourself while modifying a small thing
5. langgraph bible + draw every graph
6. build tiny projects after every lesson (or the same project that grows)

# MODULE 1

LESSON 1,2,3
Define the State as a class.
Define the Conditional Edge as a function that chooses the next node, based on current. Input: state, output: node name.
Define the Node as a function that changes the state and returns a new state.
Instantiate the StateGraph from your State class, then add nodes and edges (start from START, end with END), and build by calling .compile(). Make sure this is edited in the langgraph.json file, or you won't see in in LangSmith.

LESSON 4
State: can put list of messages! import MessageState
Node: can put tools you defined! llm.bind\_tools (in main, when defining graph, aka outside the State definition), then llm.invoke
Invokation: define llm = ChatOpenAI, define message = HumanMessage(), then .invoke(message)

LESSON 5
Use ToolNode and tools\_condition to define the tool node and to conditionally route to the tool node.
HumanMessage -> LLM -> START -> first node after start is tool-calling llm -> tool-calling LLM invokes a response -> if the response is a tool, then we route to ToolNode we defined -> ToolNode calls the tool -> END -> else if the response is natlang, we route to END.

Suppose I want to do this in a loop? I would have to conditionally route back to the tool-calling llm, right? START too-calling llm -> conditional edge to tool -> conditional edge to tool-calling llm. bidirectional edge? maybe?

What if we have more than one tool? then condiitonal edge routing would probably need to be more sophisticated??

LESSON 6
ReAct architecture: just add one edge from tool to tool-calling llm.

LESSON 7
compile your graph with a checkpointer to save the memory between graph invokations. exercise idea: try multiply that by 2, then multiply that by 4. can you pick out the first checkpoint? note: in langsmith you don't need to do thi.





# MODULE 2

LESSON 1: For State class definition, use TypedDicts, Pydantic, Dataclass.
Exercise: try defining a state class with each of these methods.

LESSON 2: In case of branching where you need to perform more than one step simultaneously, use Reducers.
You can define the state's variable as Annotated type and provide operator.add function, or a custom function if you prefer.
You can add and remove messages from the messagestate list we mentioned in module 1. (useful for history management)
Exercise: try writing a custom reducer function to remove/ add messages with branching.

LESSON 3: You can have different state schemas defined for user input and output, i.e. InputState, Output State, Overall State, then you can pass them like a filter to only have the Output State keys, i.e. builder = StateGraph(input=, output=)

LESSON 4: Trim and filter messages using RemoveMessag to filter and using trim\_messages to trim (note: inside a node function)

LESSON 5: You can make a chatbot with summarizing messages (a node) and memory checkpoints. Delete the previous messages too since you don't need them.

LESSON 6: using a SQLite checkpointer to save the checkpoints to a local db. Previously, it is saved in-memory during runtime.







MODULE 3

LESSON 1: Streaming helps you to track changes to the graph state "updates", or emit the entire state "values". Use it instead of graph.invoke(). You can also do async, not sure why...

LESSON 2: to implement human-in-the-loop, pass interrupt\_before=\["tools"] when compiling graph OR to the api through stream method.

LESSON 3: use graph.update\_state() to edit the state before interrupt. it actually uses the reducer function you defined. note: you can pass in the localhost url and run the graph in the notebook, too, using async.

LESSON 4: How to have the node interrupt itself dynamically: raise NodeInterrupt according to some condition inside the node fn.

LESSON 5: how to replay and go back to specific nodes.



MODULE 4

LESSON 1: You can create fan out fan in pattern and run nodes in parallel, but make sure the reducer function is appropriate. e.g. search Wikipedia and search web then fan-in to answer the question.

LESSON 2: 



## Exercises:

* write react architecture
* write a notebook where you try multiply by 2, then multiply that by 4. can you pick out the first checkpoint? note: in langsmith you don't need to do this.
* try defining a state class with each of the different methods.
* try writing a custom reducer function to remove/ add messages with branching.

