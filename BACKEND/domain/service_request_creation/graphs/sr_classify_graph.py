from langgraph.graph import StateGraph
from .state_schemas import State
from llm.utils.check_pointer_util import CheckpointUtil
from langchain_core.runnables import RunnableConfig
from .graph_helper import build_service_classification_prompt,build_dict_for_mandator_fields,build_prompt_extarct_mandatory,build_prompt_final_summary
from llm.factory.llm_factory import LLMFactory
from domain.service_request_creation.graphs.guard_provider import SRGuardProvider
from langgraph.types import Command
from core.decorator import handle_node_errors

guard_provider = SRGuardProvider()
llm = LLMFactory.get_open_ai_llm()

@handle_node_errors
def service_requesttype_classify_node(state: State, config: RunnableConfig):
    thread_id = config["configurable"].get("thread_id")
    request = state["request"]

    prompt = build_service_classification_prompt(state= state)

    chat_messages = [{"role": "user", "content": prompt}]
    llm_result = llm.generate(chat_messages=chat_messages)
    content_to_validate = llm_result.get("content","")
    guard_result = guard_provider.validate_classification(content_to_validate)
    update = {
        "thread_id": thread_id,
        "clarification_question" : guard_result.clarification_question,
        "is_classification_complete" :  guard_result.is_request_complete,
        "service" : guard_result.service,
        "request_type" : guard_result.request_type,
        "is_mandatory_fields_complete" : False,
        "messages": [
            {"role": "user",
             "content": prompt,
            "usage" : {
            "prompt_tokens": llm.count_tokens(prompt),
            "completion_tokens": 0,
            "total_tokens": 0,
            "time_taken_sec": 0  

        }
             },
            {
                "role": "assistant",
                "content": llm_result["content"],
                "usage": llm_result["usage"]
            }
        ]
    }
    if update["is_classification_complete"] and update["service"] is not None and update["request_type"] is not None:
        return Command(
            update=update,
            goto="mandatory_fields_extract_node"
        )
    return {
        **update,
        "user_reqs": [request],

    }


@handle_node_errors
def mandatory_fields_extract_node(state: State, config: RunnableConfig):

    found_service = state["service"]
    found_request_type = state["request_type"]
    request = state["request"]

    prompt = build_prompt_extarct_mandatory(state)
    if not prompt:
        state["is_mandatory_fields_complete"] = True
        state["data"] = {}
        return Command(
            update=state,
            goto="final_summary_node"
        )
    chat_messages = [{"role": "user", "content": prompt}]
    llm_result = llm.generate(chat_messages=chat_messages)
    content_to_validate = llm_result.get("content","")
    guard_result = guard_provider.validate_mandatory_fields(content_to_validate)

    update = {
        "clarification_question" : guard_result.clarification_question,
        "is_mandatory_fields_complete" : guard_result.is_complete,
        "data" : guard_result.data,
        "missing_fields" : guard_result.missing_fields,
        "user_reqs": [request],
        "messages": [
            {"role": "user",
             "content": prompt,
            "usage" : {
            "prompt_tokens": llm.count_tokens(prompt),
            "completion_tokens": 0,
            "total_tokens": 0,
            "time_taken_sec": 0  

        }
             },
            {
                "role": "assistant",
                "content": llm_result["content"],
                "usage": llm_result["usage"]
            }
        ]
    }

    if update["is_mandatory_fields_complete"] and state["is_classification_complete"]:
        return Command(
            update=update,
            goto="final_summary_node"
        )

    return {
        **state,
      **update
    }

@handle_node_errors
def router_node(state: State):
    if (
        state.get("is_classification_complete")
        and state.get("service")
        and state.get("request_type")
    ):
        return Command(goto="mandatory_fields_extract_node")

    return Command(goto="service_requesttype_classify_node")

@handle_node_errors
def final_summary_node(state : State):
    prompt = build_prompt_final_summary(state)
    chat_messages = [{"role": "user", "content": prompt}]
    llm_result = llm.generate(chat_messages=chat_messages)
    content_to_validate = llm_result.get("content","")
    guard_result = guard_provider.validate_final_summary(content_to_validate)
    return {
        **state,
        "final_summary" : guard_result.final_summary
    }

def build_graph():
    graph = StateGraph(State)
    graph.add_node("router_node", router_node)

    graph.add_node("service_requesttype_classify_node", service_requesttype_classify_node)
    graph.add_node("mandatory_fields_extract_node", mandatory_fields_extract_node)
    graph.add_node("final_summary_node",final_summary_node)
    graph.set_entry_point("router_node")

    return graph.compile(checkpointer=CheckpointUtil._checkpointer)


