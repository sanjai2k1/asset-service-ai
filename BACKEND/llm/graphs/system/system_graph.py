from typing import TypedDict
from langgraph.graph import StateGraph

from llm.chains.system.system_chain import SystemChain
from langchain_core.runnables import RunnableConfig


systemcheck = SystemChain()


def llm_check_node(state : dict, config: RunnableConfig):
    thread_id = config["configurable"].get("thread_id")
    
    print(f"[NODE DEBUG] Running node with Thread ID: {thread_id}")
    result = systemcheck.run(thread_id=thread_id)



    return result


def build_graph():

    graph = StateGraph(dict)

    graph.add_node(
        "llmcheck",
        llm_check_node
    )

    graph.set_entry_point(
        "llmcheck"
    )

    graph.set_finish_point(
        "llmcheck"
    )

    return graph.compile()